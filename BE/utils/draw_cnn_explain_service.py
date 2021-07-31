import pandas as pd
import numpy as np
import scipy as sp
import shap
import gc
import matplotlib
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from scipy.sparse import issparse
from matplotlib.colors import LinearSegmentedColormap

matplotlib.use('Agg')

def kmeans(X, k, round_values=True):
    """ Summarize a dataset with k mean samples weighted by the number of data points they
    each represent.
    Parameters
    ----------
    X : numpy.array or pandas.DataFrame or any scipy.sparse matrix
        Matrix of data samples to summarize (# samples x # features)
    k : int
        Number of means to use for approximation.
    round_values : bool
        For all i, round the ith dimension of each mean sample to match the nearest value
        from X[:,i]. This ensures discrete features always get a valid value.
    Returns
    -------
    DenseData object.
    """

    group_names = [str(i) for i in range(X.shape[1])]
    if str(type(X)).endswith("'pandas.core.frame.DataFrame'>"):
        group_names = X.columns
        X = X.values

    # in case there are any missing values in data impute them
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    X = imp.fit_transform(X)

    kmeans = KMeans(n_clusters=k, random_state=0).fit(X)

    if round_values:
        for i in range(k):
            for j in range(X.shape[1]):
                xj = X[:, j].toarray().flatten() if issparse(X) else X[:, j]  # sparse support courtesy of @PrimozGodec
                ind = np.argmin(np.abs(xj - kmeans.cluster_centers_[i, j]))
                kmeans.cluster_centers_[i, j] = X[ind, j]
    return DenseData(kmeans.cluster_centers_, group_names, None, 1.0 * np.bincount(kmeans.labels_))


class Instance:
    def __init__(self, x, group_display_values):
        self.x = x
        self.group_display_values = group_display_values


def convert_to_instance(val):
    if isinstance(val, Instance):
        return val
    else:
        return Instance(val, None)


class InstanceWithIndex(Instance):
    def __init__(self, x, column_name, index_value, index_name, group_display_values):
        Instance.__init__(self, x, group_display_values)
        self.index_value = index_value
        self.index_name = index_name
        self.column_name = column_name

    def convert_to_df(self):
        index = pd.DataFrame(self.index_value, columns=[self.index_name])
        data = pd.DataFrame(self.x, columns=self.column_name)
        df = pd.concat([index, data], axis=1)
        df = df.set_index(self.index_name)
        return df


def convert_to_instance_with_index(val, column_name, index_value, index_name):
    return InstanceWithIndex(val, column_name, index_value, index_name, None)


def match_instance_to_data(instance, data):
    assert isinstance(instance, Instance), "instance must be of type Instance!"

    if isinstance(data, DenseData):
        if instance.group_display_values is None:
            instance.group_display_values = [instance.x[0, group[0]] if len(group) == 1 else "" for group in
                                             data.groups]
        assert len(instance.group_display_values) == len(data.groups)
        instance.groups = data.groups


class Model:
    def __init__(self, f, out_names):
        self.f = f
        self.out_names = out_names


def convert_to_model(val):
    if isinstance(val, Model):
        return val
    else:
        return Model(val, None)


def match_model_to_data(model, data):
    assert isinstance(model, Model), "model must be of type Model!"

    try:
        if isinstance(data, DenseDataWithIndex):
            out_val = model.f(data.convert_to_df())
        else:
            out_val = model.f(data.data)
    except:
        print("Provided model function fails when applied to the provided data set.")
        raise

    if model.out_names is None:
        if len(out_val.shape) == 1:
            model.out_names = ["output value"]
        else:
            model.out_names = ["output value " + str(i) for i in range(out_val.shape[0])]

    return out_val


class Data:
    def __init__(self):
        pass


class SparseData(Data):
    def __init__(self, data, *args):
        num_samples = data.shape[0]
        self.weights = np.ones(num_samples)
        self.weights /= np.sum(self.weights)
        self.transposed = False
        self.groups = None
        self.group_names = None
        self.groups_size = data.shape[1]
        self.data = data


class DenseData(Data):
    def __init__(self, data, group_names, *args):
        self.groups = args[0] if len(args) > 0 and args[0] is not None else [np.array([i]) for i in
                                                                             range(len(group_names))]

        l = sum(len(g) for g in self.groups)
        num_samples = data.shape[0]
        t = False
        if l != data.shape[1]:
            t = True
            num_samples = data.shape[1]

        valid = (not t and l == data.shape[1]) or (t and l == data.shape[0])
        assert valid, "# of names must match data matrix!"

        self.weights = args[1] if len(args) > 1 else np.ones(num_samples)
        self.weights /= np.sum(self.weights)
        wl = len(self.weights)
        valid = (not t and wl == data.shape[0]) or (t and wl == data.shape[1])
        assert valid, "# weights must match data matrix!"

        self.transposed = t
        self.group_names = group_names
        self.data = data
        self.groups_size = len(self.groups)


class DenseDataWithIndex(DenseData):
    def __init__(self, data, group_names, index, index_name, *args):
        DenseData.__init__(self, data, group_names, *args)
        self.index_value = index
        self.index_name = index_name

    def convert_to_df(self):
        data = pd.DataFrame(self.data, columns=self.group_names)
        index = pd.DataFrame(self.index_value, columns=[self.index_name])
        df = pd.concat([index, data], axis=1)
        df = df.set_index(self.index_name)
        return df


def convert_to_data(val, keep_index=False):
    if isinstance(val, Data):
        return val
    elif type(val) == np.ndarray:
        return DenseData(val, [str(i) for i in range(val.shape[1])])
    elif str(type(val)).endswith("'pandas.core.series.Series'>"):
        return DenseData(val.values.reshape((1, len(val))), list(val.index))
    elif str(type(val)).endswith("'pandas.core.frame.DataFrame'>"):
        if keep_index:
            return DenseDataWithIndex(val.values, list(val.columns), val.index.values, val.index.name)
        else:
            return DenseData(val.values, list(val.columns))
    elif sp.sparse.issparse(val):
        if not sp.sparse.isspmatrix_csr(val):
            val = val.tocsr()
        return SparseData(val)
    else:
        assert False, "Unknown type passed as data object: " + str(type(val))


class Link:
    def __init__(self):
        pass


class IdentityLink(Link):
    def __str__(self):
        return "identity"

    @staticmethod
    def f(x):
        return x

    @staticmethod
    def finv(x):
        return x


class LogitLink(Link):
    def __str__(self):
        return "logit"

    @staticmethod
    def f(x):
        return np.log(x / (1 - x))

    @staticmethod
    def finv(x):
        return 1 / (1 + np.exp(-x))


def convert_to_link(val):
    if isinstance(val, Link):
        return val
    elif val == "identity":
        return IdentityLink()
    elif val == "logit":
        return LogitLink()
    else:
        assert False, "Passed link object must be a subclass of iml.Link"


class CNNExplain():

    def __init__(self, size=30, titlesize=28, dest='tmp/vgg16_explain.jpg'):
        self.dest = dest

        colors = []
        for l in np.linspace(1, 0, 100):
            colors.append((30. / 255, 136. / 255, 229. / 255, l))
        for l in np.linspace(0, 1, 100):
            colors.append((255. / 255, 13. / 255, 87. / 255, l))
        self.red_transparent_blue = LinearSegmentedColormap.from_list("red_transparent_blue", colors)

        if size > 0:
            plt.rc('font', size=size)

        if titlesize > 0:
            plt.rc('axes', titlesize=titlesize)

    def get_explainer(self, model, background):
        return shap.DeepExplainer(model, background)

    def get_explain_image(self, e, data):
        ex_data = np.asarray([data])
        shap_values = e.shap_values(ex_data, check_additivity=False)
        feature_image_dir = self.image(shap_values, -ex_data)
        gc.collect()
        return feature_image_dir

    def image(self, shap_values, pixel_values=None, labels=None, width=20, labelpad=None, show=True):
        # support passing an explanation object
        if str(type(shap_values)).endswith("Explanation'>"):
            shap_exp = shap_values
            feature_names = [shap_exp.feature_names]
            ind = 0
            if len(shap_exp.base_values.shape) == 2:
                shap_values = [shap_exp.values[..., i] for i in range(shap_exp.values.shape[-1])]
            else:
                raise Exception("Number of outputs needs to have support added!! (probably a simple fix)")
            if pixel_values is None:
                pixel_values = shap_exp.data
            if labels is None:
                labels = shap_exp.output_names

        multi_output = True
        if type(shap_values) != list:
            multi_output = False
            shap_values = [shap_values]

        # make sure labels
        if labels is not None:
            labels = np.array(labels)
            assert labels.shape[0] == shap_values[0].shape[0], "Labels must have same row count as shap_values arrays!"
            if multi_output:
                assert labels.shape[1] == len(shap_values), "Labels must have a column for each output in shap_values!"
            else:
                assert len(labels.shape) == 1, "Labels must be a vector for single output shap_values."

        label_kwargs = {} if labelpad is None else {'pad': labelpad}

        # plot our explanations
        x = pixel_values
        fig_size = np.array([3 * (len(shap_values) + 1), 2.5 * (x.shape[0] + 1)])
        if fig_size[0] > width:
            fig_size *= width / fig_size[0]
        fig, axes = plt.subplots(nrows=x.shape[0], ncols=len(shap_values) + 1, figsize=(22, 22))
        if len(axes.shape) == 1:
            axes = axes.reshape(1, axes.size)
        for row in range(x.shape[0]):
            x_curr = x[row].copy()

            # make sure we have a 2D array for grayscale
            if len(x_curr.shape) == 3 and x_curr.shape[2] == 1:
                x_curr = x_curr.reshape(x_curr.shape[:2])
            if x_curr.max() > 1:
                x_curr = x_curr / 255.

            # get a grayscale version of the image
            if len(x_curr.shape) == 3 and x_curr.shape[2] == 3:
                x_curr_gray = (
                        0.2989 * x_curr[:, :, 0] + 0.5870 * x_curr[:, :, 1] + 0.1140 * x_curr[:, :, 2])  # rgb to gray
                x_curr_disp = x_curr
            elif len(x_curr.shape) == 3:
                x_curr_gray = x_curr.mean(2)

                # for non-RGB multi-channel data we show an RGB image where each of the three channels is a scaled k-mean center
                flat_vals = x_curr.reshape([x_curr.shape[0] * x_curr.shape[1], x_curr.shape[2]]).T
                flat_vals = (flat_vals.T - flat_vals.mean(1)).T
                means = kmeans(flat_vals, 3, round_values=False).data.T.reshape([x_curr.shape[0], x_curr.shape[1], 3])
                x_curr_disp = (means - np.percentile(means, 0.5, (0, 1))) / (
                        np.percentile(means, 99.5, (0, 1)) - np.percentile(means, 1, (0, 1)))
                x_curr_disp[x_curr_disp > 1] = 1
                x_curr_disp[x_curr_disp < 0] = 0
            else:
                x_curr_gray = x_curr
                x_curr_disp = x_curr

            axes[row, 0].imshow(x_curr_disp, cmap=plt.get_cmap('gray'))
            axes[row, 0].axis('off')
            if len(shap_values[0][row].shape) == 2:
                abs_vals = np.stack([np.abs(shap_values[i]) for i in range(len(shap_values))], 0).flatten()
            else:
                abs_vals = np.stack([np.abs(shap_values[i].sum(-1)) for i in range(len(shap_values))], 0).flatten()
            max_val = np.nanpercentile(abs_vals, 99.9)
            for i in range(len(shap_values)):
                if labels is not None:
                    axes[row, i + 1].set_title(labels[row, i], **label_kwargs)
                sv = shap_values[i][row] if len(shap_values[i][row].shape) == 2 else shap_values[i][row].sum(-1)
                axes[row, i + 1].imshow(x_curr_gray, cmap=plt.get_cmap('gray'), alpha=0.15,
                                        extent=(-1, sv.shape[1], sv.shape[0], -1))
                im = axes[row, i + 1].imshow(sv, cmap=self.red_transparent_blue, vmin=-max_val, vmax=max_val)
                axes[row, i + 1].axis('off')

        cb = fig.colorbar(im, ax=np.ravel(axes).tolist(), label="Explain value", orientation="horizontal", aspect=20)
        cb.outline.set_visible(False)
        if show:
            plt.savefig(self.dest)

        plt.close()
        return self.dest
