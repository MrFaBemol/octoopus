import itertools
import logging
_logger = logging.getLogger(__name__)


# Todo: clean this shit

# Constants
SEPARATOR_MAIN = "@"
SEPARATOR_SECOND = "-"
SEPARATOR_THIRD = ":"       # Todo: change to comma ,

def generate_all_ensembles(instruments_slots: list) -> list:
    """
        Generate all possible combinations with instruments slots
        :return: list[] of dict{}: instrument_id: qty
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

def get_search_key(instrument_slots: list, min_instrument_qty: int = 0, max_instrument_qty: int = 0) -> str:
    """
        Generated a search key as follows :
            performers_quantity@
            slot possibilities separated by ":" (ex "1:2:3:4:5")
            all slots separated by "-"

        Sort all slots before.

        Example :
            Input  :    [[1], [2, 3], [0], [2, 3], [2, 4]]
            Output :    6@0-0-1-2:3-2:3-2:4
    """

    min_instrument_qty = max(min_instrument_qty, len(instrument_slots))
    if max_instrument_qty and max_instrument_qty < min_instrument_qty:
        _logger.warning("Max performers qty is lower than min (passed: %s, min: %s). Automatic update has been made" % (max_instrument_qty, min_instrument_qty))
    max_instrument_qty = max(min_instrument_qty, max_instrument_qty)


    # We sort the id of possible instruments for each slot, then the slots themselves
    instruments_slots = sorted(map(lambda slot: sorted(slot), instrument_slots))

    key = "%s%s%s" % (
        "%s%s%s" % (min_instrument_qty, SEPARATOR_SECOND, max_instrument_qty),
        SEPARATOR_MAIN,
        SEPARATOR_SECOND.join([SEPARATOR_THIRD.join([str(ins) for ins in slot]) for slot in instruments_slots])
    )
    return key

def get_ensemble_search_key(ensemble_dict: dict, instrument_qty: int = 0) -> str:
    """
        Generated an ensemble search key as follows :
            performers_quantity@
            => instrument_id ":" quantity for each entry separated by "-"

        Example:
            Input  :    {0: 2, 1: 1, 2: 2, 4: 1}
            Output :    6@0:2-1:1-2:2-4:1
    """
    if instrument_qty and instrument_qty < sum(ensemble_dict.values()):
        raise IndexError("Not enough performers (passed: %s, expected: %s min)" % (instrument_qty, sum(ensemble_dict.values())))

    performers_quantity = max(instrument_qty, sum(ensemble_dict.values()))
    key = "%s%s%s" % (
        performers_quantity,
        SEPARATOR_MAIN,
        SEPARATOR_SECOND.join(["%s%s%s" % (instrument_id, SEPARATOR_THIRD, qty) for instrument_id, qty in ensemble_dict.items()])
    )
    return key





def get_ensemble_domain(ensemble_key):
    pass




# --------------------------------------------
#                   MISC
# --------------------------------------------

# Todo: remove self and find a way to do it somehow
def categories_to_instruments(self, instrument_slots):
    for i, slot in enumerate(instrument_slots):
        all_ins = self.env['instrument'].browse(slot)
        categories = all_ins.filtered('is_category')
        instruments = all_ins - categories
        instrument_slots[i] = (instruments | categories.all_instrument_ids).ids
    return instrument_slots

def get_slot_by_type(instrument_slots):
    fixed_slots = list()
    variable_slots = list()
    for slot in instrument_slots:
        if len(slot) == 1:
            fixed_slots.append(slot)
        elif len(slot) > 1:
            variable_slots.append(slot)
    return fixed_slots, variable_slots


# ------------------------------------------


