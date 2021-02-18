.PHONY: run call

run:
	uvicorn api:app --port 7777 --reload

call:
	@curl localhost:7777/write-book --data '{"book_title": "something"}'
