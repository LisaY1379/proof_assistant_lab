FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY main /app/main
COPY data/general/strategy_hierarchy.json /app/data/general/strategy_hierarchy.json

ENV HOST=0.0.0.0
ENV PORT=7860

EXPOSE 7860

CMD ["python", "main/agent_server.py"]
