import json
import numpy as np
import os
import io


def dice_score(ref, pred):
    # from https://stackoverflow.com/questions/49759710/calculating-dice-co-efficient-between-two-random-images-of-same-size
    if ref.shape != pred.shape:
        raise ValueError("Shape mismatch: img and img2 must have to be of the same shape.")
    else:
        intersection = np.logical_and(ref, pred)
        value = (2. * intersection.sum()) / (ref.sum() + pred.sum())
    return value

def dice_list(reference_json, user_json, image_width=1024, image_height=1024):
    f_reference = open(reference_json)
    if isinstance(user_json, str):
        f_user = open(user_json)
    else:
        f_user = io.StringIO(user_json.getvalue().decode("utf-8"))
#        f_user = json.load(stringio)

    data_reference = json.load(f_reference)
    data_user = json.load(f_user)

    list_dice_scores = []
    # if "covid27" in reference_json:
    gt_patients_list = data_reference["_via_img_metadata"]
    user_patients_list = data_user["_via_img_metadata"]
    for key in gt_patients_list:
        if key in user_patients_list:
            np_reference = np.zeros([image_width, image_height])
            np_user = np.zeros([image_width, image_height])
            for region in gt_patients_list[key]["regions"]:
                if region['shape_attributes']['name'] == 'rect':
                    x_start = region['shape_attributes']['x']
                    y_start = region['shape_attributes']['y']
                    x_end = region['shape_attributes']['width'] + x_start
                    y_end = region['shape_attributes']['height'] + y_start

                    np_reference[x_start:x_end, y_start:y_end] = 1
                else: # doesn't have rect type of region so we should skip it
                    break
            for region in user_patients_list[key]["regions"]:
                if region['shape_attributes']['name'] == 'rect':

                    x_start = region['shape_attributes']['x']
                    y_start = region['shape_attributes']['y']
                    x_end = region['shape_attributes']['width'] + x_start
                    y_end = region['shape_attributes']['height'] + y_start

                    np_user[x_start:x_end, y_start:y_end] = 1

            dice_score_patient = dice_score(np_reference, np_user)
            if not np.isnan(dice_score_patient):
                list_dice_scores.append(dice_score_patient)
            else: # reference didn't had rect but user drew rect
                list_dice_scores.append(0)
        else:
            for region in gt_patients_list[key]["regions"]:
                if region['shape_attributes']['name'] == 'rect':
                    list_dice_scores.append(0)
                    print("Not segmented by used")
                else:
                    print("Not rect tool")
    return list_dice_scores

def get_score_all_users(directory, ground_truth_file, user_files_list):
    reference_json = os.path.join(directory, ground_truth_file)
    scores_users = []
    for user_file in user_files_list:
        user_json = os.path.join(directory, user_file)
        dice_scores = dice_list(reference_json, user_json)
        user_score = round(np.sum(np.asarray(dice_scores)) * 10)
        scores_users.append(user_score)
    order_users = np.argsort(scores_users)
    return order_users, scores_users


# if __name__ == '__main__':
#     # example of input and call to get order and scores
#     # inputs are directory where files are located, ground truth json filename, list of json users annotations filenames
#     order, score = get_score_all_users('/Users/joaosantinha/Downloads',
#                                        'via_project_9Dec2020_15h40m_Les_ground_truth.json',
#                                        ['via_project_8Dec2020_15h28m_jane_with_missing_keys.json',
#                                         'via_project_18May2021_13h3m_Pedro.json',
#                                         'via_project_20May2021_10h53m-6_Lilli.json'])
#     print('Order: ', order+1, '\nScore: ', score)
