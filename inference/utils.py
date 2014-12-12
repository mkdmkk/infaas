__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'

def convert_to_sequential_data(dataset):
    contexts_sequential_array = []
    # if contexts_res.count() > 0:
    # first_time = contexts_res[0]["time"]

    # dt_util = DateTimeUtil()
    for context_res in dataset:
        # dt_diff = dt_util.get_difference_as_seconds(first_time, context_res["time"]);
        # contexts_sequential_array.append([
        #     dt_diff,
        #     context_res["data"]["x"],
        #     context_res["data"]["y"],
        #     context_res["data"]["z"]])
        # contexts_sequential_array.append(dt_diff)
        contexts_sequential_array.append(float(context_res["data"]["x"]))
        contexts_sequential_array.append(float(context_res["data"]["y"]))
        contexts_sequential_array.append(float(context_res["data"]["z"]))

    return contexts_sequential_array
