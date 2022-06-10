from flask import Flask, render_template
import pandas as pd
from clickhouse_driver import Client


api = Flask(
	__name__,
	static_url_path='',
	static_folder='static',
	template_folder='templates'
)

ch_client = Client(host="host.docker.internal")
EXPECTED_LABELS_COUNT = 3


def get_queries_per_our_chart_data():
	global ch_client, EXPECTED_LABELS_COUNT
	queries_per_house_ch_query = """
	SELECT 
		date_trunc('hour', ts), prediction, count(vector)
	FROM prod.query_logs
		GROUP BY prediction, dt, date_trunc('hour', ts)
		order by date_trunc('hour', ts) asc
	"""

	data = ch_client.execute(queries_per_house_ch_query)
	t = pd.DataFrame(data, columns=["date", "prediction", "count"])
	t = pd.pivot_table(t, index="date", columns="prediction", fill_value=0.0)
	print(t.index)
	return t.index.strftime("%H:%M %m/%d/%Y"), t.iloc[:, 0].values, t.iloc[:, 1].values, t.iloc[:, 2].values


def get_all_queries_count_by_label():
	global ch_client
	pie_data_query = """
	SELECT 
		prediction, count(prediction)
	FROM prod.query_logs
		GROUP BY prediction
	ORDER BY prediction asc
	"""
	data = ch_client.execute(pie_data_query)
	print(data)
	return list(map(lambda tup: tup[1], data))


@api.route("/", methods=['GET'])
def get_token():
	x, y1, y2, y3 = get_queries_per_our_chart_data()
	pie_data = get_all_queries_count_by_label()
	return render_template(
		"main_page.html",
		labels=list(x),
		safe_queries=list(y1),
		sql_injections_queries=list(y2),
		eval_injections_queries=list(y3),
		pie_data=pie_data
	)


if __name__ == '__main__':
	api.run()
