from okapy import fetch, generate

initial_data = fetch(all_pages=True)
generate(initial_data=initial_data, id_suffix="-1")
