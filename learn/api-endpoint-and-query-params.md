# API Endpoint and Query Params

An API endpoint is a URL you send a request to in order to get data.

Query parameters are key-value settings added to the URL (like `?where=1%3D1&outFields=*`) that control what data is returned.

Why this matters here: ArcGIS FeatureServer data is pulled from a `query` endpoint, and your parameters decide record limit, fields, format, and geometry output.
