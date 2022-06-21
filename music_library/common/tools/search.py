import itertools


def generate_all_ensembles(instruments_slots):
    """
        Generate all possible combinations with instruments slots
        :return: list[] of dict{}: key = instrument_id, value = qty
    """
    # Generate all combinations
    all_combinations = list(itertools.product(*instruments_slots))
    all_ensembles = list()

    # We go through the possible combinations
    for ensemble in all_combinations:
        instrument_ids = set(ensemble)
        ensemble_dict = dict(zip(instrument_ids, [ensemble.count(instrument_id) for instrument_id in instrument_ids]))

        # If we didn't save this ensemble yet, we do
        if ensemble_dict not in all_ensembles:
            all_ensembles.append(ensemble_dict)
    return all_ensembles

def get_search_key(instrument_slots, performer_qty=0):
    """
        Generated a search key as follow :
            performers_quantity@
            slot possibilities separated by ":" (ex "1:2:3:4:5")
            all slots separated by "-"

        Sort all slots before.

        Example :
            Input  :    [[1], [2, 3], [0], [2, 3], [2, 4]]
            Output :    6@0-0-1-2:3-2:3-2:4
    """

    if performer_qty and performer_qty < len(instrument_slots):
        raise IndexError("Not enough performers (passed: %s, expected: %s min)" % (performer_qty, len(instrument_slots)))

    performers_quantity = max(performer_qty, len(instrument_slots))
    instrument_slots += [[0] for i in range(performers_quantity - len(instrument_slots))]

    # We sort the id of possible instruments for each slot, then the slots themself
    instruments_slots = sorted(map(lambda slot: sorted(slot), instrument_slots))

    key = "%s@%s" % (
        performers_quantity,
        "-".join([":".join([str(ins) for ins in slot]) for slot in instruments_slots])
    )
    return key

def get_ensemble_search_key(ensemble_dict, performer_qty=0):
    """
        Generated an ensemble search key as follow :
            performers_quantity@
            => instrument_id ":" quantity         for each entry
            each entry separated by "-"

        Example :
            Input  :    {0: 2, 1: 1, 2: 2, 4: 1}
            Output :    6@0:2-1:1-2:2-4:1
    """
    if performer_qty and performer_qty < sum(ensemble_dict.values()):
        raise IndexError("Not enough performers (passed: %s, expected: %s min)" % (performer_qty, sum(ensemble_dict.values())))

    performers_quantity = max(performer_qty, sum(ensemble_dict.values()))
    key = "%s@%s" % (
        performers_quantity,
        "-".join(["%s:%s" % (instrument_id, qty) for instrument_id, qty in ensemble_dict.items()])
    )
    return key



# ------------------------------------------



# instruments2 = [[1], [2, 3], [0], [2, 3], [2, 4]]
# a = instruments2.copy()
#
# print(get_search_key(a, 6))
#
# print()
# ensembles = get_all_ensembles(a)
# print(ensembles)
# print(len(ensembles))
# print()
# #
# for e in ensembles:
#     print("%s => %s" % (get_ensemble_search_key(e), e))


