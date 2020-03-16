import time
import requests
import pandas as pd

def get_url(url_type):
    """
    This function returns the base url for further data retrival
    :param url_type:
    :return: base_url
    """
    base_url = "https://api.pushshift.io/reddit/" + url_type + "/search?"
    return base_url


def get_params(subreddit, rsize, header, before=None):
    """

    :param subreddit:
    :param rsize:
    :param header:
    :param before:
    :return:
    """
    params = {
        "subreddit": subreddit,
        "size": rsize,
        "header": header,
        "sort": "desc"
    }

    if before:
        params.update({"before": before})

    return params


def get_data(subreddit, size, header, end_points, before=None):
    """

    :param subreddit:
    :param size:
    :param header:
    :param end_points:
    :param before:
    :return:
    """
    url = get_url(end_points)
    params = get_params(subreddit, size, header, before)
    res = requests.get(url, params)
    if res.status_code != 200:
        print(f'Error Code: {res.status_code}')
    else:
        return pd.DataFrame(res.json()['data'])


def save_data(data, subreddit, end_points, **kwargs):
    """

    :param data:
    :param subreddit:
    :param end_points:
    :param kwargs:
    :return:
    """
    data.to_csv(kwargs.get("file_path") + subreddit + "_" + end_points + "_" + str(kwargs.get("run_number")) + ".csv",
                index=False)


def get_last_time(data):
    """

    :param data:
    :return:
    """
    return min(data["created_utc"])  ##capture the last created record


def get_required_data(data, end_points, **kwargs):
    """

    :param data:
    :param end_points:
    :param kwargs:
    :return:
    """
    fields_to_download = kwargs.get("fields_to_download")
    req_cols = []
    for cols in fields_to_download[end_points]:
        if cols in data.columns:
            req_cols.append(cols)
    data = data[req_cols]
    data.sort_values(by="created_utc", ascending=True)
    # data["created_utc"].drop_duplicates(inplace=True)
    return data


def check_columns(df, full_df):
    """

    :param df:
    :param full_df:
    :return:
    """
    if len(df.columns) > len(full_df.columns):
        for cols in df.columns:
            if cols not in full_df.columns:
                full_df[cols] = None
    else:
        for cols in full_df.columns:
            if cols not in df.columns:
                df[cols] = None


def get_save_all_data(subreddit, end_points, **kwargs):
    """

    :param subreddit:
    :param end_points:
    :param kwargs:
    :return:
    """
    no_of_records = kwargs.get("no_of_rec_per_cycle")
    no_of_cycles = int(kwargs.get("total_no_of_records") / no_of_records)
    full_df = get_data(subreddit, no_of_records, "someone", end_points)
    full_df = get_required_data(full_df, end_points, **kwargs)
    for cycle in range(1, no_of_cycles):
        str_cycle = str(cycle)
        if cycle == 1:
            before = get_last_time(full_df)
        else:
            before = get_last_time(df)
        print("Going to read data for " + subreddit + " " + end_points + " ...." + str_cycle)
        print("Sleeping for {} secs ...".format(kwargs.get("time_delay")))
        time.sleep(kwargs.get("time_delay"))
        print("Woken up .... ")
        df = get_data(subreddit, no_of_records, "someone", end_points, before)
        df = get_required_data(df, end_points, **kwargs)
        if df.shape[1] != full_df.shape[1]:
            check_columns(df, full_df)
        full_df = pd.concat((full_df, df), axis=0)
        # full_df.reset_index(inplace=True)
    print("Saving the data for " + subreddit + " " + end_points + " ....")
    save_data(full_df, subreddit, end_points, **kwargs)
    print("Saved the data for " + subreddit + " " + end_points + " ....")


def download_subreddits(**kwargs):
    """

    :param kwargs:
    :return:
    """
    subreddits = kwargs.get("subreddits")
    endpoints = kwargs.get("endpoints")

    for subs in subreddits:
        for eps in endpoints:
            get_save_all_data(subs, eps, **kwargs)
    print("Completed downloading all data successfully...")


if __name__ == "__main__":
    params = {
        # Run number - make user to update this every time other wise it will overwrite existing records
        "run_number": 10,

        # subreddits to download, even if it is 1 , it has to be a list
        "subreddits": ["evolution", "creation", "DebateEvolution"],

        # endpoints to download, even if it is 1 , it has to be a list
        "endpoints": ["submission", "comment"],

        # where to download
        "file_path": "../datasets/",

        # number of records to download each cycle
        "no_of_rec_per_cycle": 1000,

        # total number of records to be downloaded. Total no of records that will be stored in each file as .csv
        "total_no_of_records": 10_000,

        # 3 seconds wait till the next run
        "time_delay": 3,

        # choose fields to download for each end points
        "fields_to_download": {
            "submission": ["subreddit", "id", "author", "author_flair_text", "author_fullname", "domain", "link_flair_text", "title",
                           "selftext", "num_comments", "created_utc", "full_link"],
            "comment": ["parent_id", "link_id", "body", "created_utc"],
        }
    }



    # Downloading the data
    download_subreddits(**params)


