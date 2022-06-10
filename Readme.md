### About

This project is aimed to solve injection queries classification problem given by https://slot-ml.com/.

You can get analysis report via special analytical service host on http://127.0.0.1:5000/ address by default.
Fo this purposes, run docker image from `service/analysis_service` folder.

### Structure

All research notebooks can be found in the `research` folder.

`service` folder have containerized service with latest model.
All users queries are saved in the clickhouse database.

#### Service config

In order to run service, you need firstly specify your `user_token` in `service/model/model.env` file.

Use mock traffic generator for testing purposes: set `TRAFFIC_URL=http://mock_query_generator:5000/`.
Mock traffic generator will always return the same query. Also it supports all API's from real service (https://slot-ml.com/).



## Background review

TF-IDF classification approach is described in this study.

Article: https://revistageintec.net/wp-content/uploads/2022/02/1939.pdf 


Same problem is solved here, however, it's a supervised learning case, since all train samples have labels.

Article: https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=1649&context=etd_projects


A big study were made, open-source code was provided.

Article: https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=1727&context=etd_projects

Code: https://github.com/tungpv98/Detect-Sql-Injection-by-Machine-Learning