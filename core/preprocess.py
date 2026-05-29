def build_tags(df):
    df["tags"] = (
        df["genres"].apply(lambda x: " ".join(x)) + " " +
        df["keywords"].apply(lambda x: " ".join(x)) + " " +
        df["cast"].apply(lambda x: " ".join(x)) + " " +
        df["overview"].fillna("")
    )
    return df
