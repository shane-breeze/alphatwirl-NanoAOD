"""
Handle the dataframe configuration
"""
from alphatwirl.binning import Binning, Echo
#from alphatwirl_interface.weighters import  WeightCalculatorProduct
import copy


def prepare_dataframe_configs(weights=[]):
    '''
        Creates the definition/config of the data frame (DF).

        :return a list of DF configs
    '''
    # Set up categorical binning
    jetpt_bin = Binning(boundaries=range(0, 1000, 20))
    njetbin = Echo()

    # a list of DF configs
    base = dict(
                keyAttrNames=('Jet_pt', 'nJet'),
                keyOutColumnNames=('jetpt', 'njet'),
                binnings=(jetpt_bin, njetbin),
                )

    df_configs = {"data": base}
    #else:
    #    df_configs = {}

    #    # List of weight branches that are multiplied together for the final event weight
    #    #
    #    # TODO: Storing the product of these weights as weight_nominal for each
    #    # event would be more efficient, but this needs communication or a
    #    # common interface between a nominal weight scribbler and the DF
    #    # configuration

    #    # Build a dictionary for all the combinations of weights we need to check for systematics
    #    weight_combinations = {"nominal": weights, "unweighted": []}
    #    for weight in weights:
    #        for variation in ["up", "down"]:
    #            variation_name = "{}_{}".format(weight, variation)
    #            weight_combinations[variation_name] = weights + [variation_name]

    #    df_configs = {}
    #    for name, weight_list in weight_combinations.items():
    #        config = copy.copy(base)
    #        if weight_list:
    #            config["weight"] = WeightCalculatorProduct(weight_list)
    #        df_configs[name] = config

    return df_configs
