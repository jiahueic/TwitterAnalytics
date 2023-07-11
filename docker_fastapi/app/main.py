
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers = ["hi"],
)

import couchdb
import time

couch1 = couchdb.Server('http://admin:admin@172.26.135.89:5984')
db1 = couch1["mastadon"]
db3 = couch1["twittersa3_f"]

couch2 = couchdb.Server('http://admin:admin@172.26.135.152:5984')
db2 = couch2["twitter"]

couch3 = couchdb.Server('http://admin:YOURPASSWORD@172.26.129.91:5984')
db4 = couch3["thuge"]

mentalhealth_tags = ["anxiety", "depression", "ptsd", "bipolar", "schizophrenia", "paranoia", "psychosis", "eating"]

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())

@cache()
async def get_cache():
    return 1

@app.get("/")
async def read_root():
    return {"Hello_2"}


@app.get("/happiness_sa3")
@cache(expire=60*60*24*30)
async def get_happiness():

    happiness = []
    time0 = time.time()

    query_result = db3.view('mydesigndoc/sa3_sentiment_map', group = True, reduce = True, timeout = 5000)
    time_q = time.time()
    for x in query_result:
        data = {}
        data["sa3Code"] = x.key
        data["happiness"] = x.value
        happiness.append(data)
    time_a = time.time()
    # happiness.append(time_q-time0)
    # happiness.append(time_a-time_q)
    return happiness



# @app.get("/mastodon_tags/top_100")
# @cache(expire=60*60*12)
# async def get_count():
#     query_result = db1.view('mydesigndoc/tag_count_map', group = True, reduce = True)
#     tag_counts = {}
#     for x in query_result:
#         tag_counts[x.key] = x.value
#     sorted_tags = sorted(tag_counts, key = tag_counts.get, reverse=True)

#     output = []

#     for tag in sorted_tags[:100]:
#         count = tag_counts[tag]
#         xx = {}
#         xx[tag] = count
#         output.append(xx)

#     return output



@app.get("/mastodon_tags/top_10")
@cache(expire=60*60*24*30)
async def get_count_1():
    time0 = time.time()
    query_result = db1.view('mydesigndoc/tag_count_map', group = True, reduce = True)
    time_q = time.time()
    tag_counts = {}
    for x in query_result:
        tag_counts[x.key] = x.value
    sorted_tags = sorted(tag_counts, key = tag_counts.get, reverse=True)
    time_s = time.time()


    output = []

    for tag in sorted_tags[:10]:
        count = tag_counts[tag]
        xx = {}
        xx[tag] = count
        output.append(xx)
    time_a = time.time()

    # output.append(time_q-time0)
    # output.append(time_s-time_q)
    # output.append(time_a-time_s)

    return output



@app.get("/mastodon_tags/mentalhealth_about")
#@cache(expire=60*60*12)
async def get_count_2():
    time0 = time.time()
    tag_counts = {}

    for x in  mentalhealth_tags:
        query_result = db1.view('mydesigndoc/tag_count_map', group = True, reduce = True,  key = x)
        time_q = time.time()

        for x in query_result:
            if x.key in mentalhealth_tags:
                tag_counts[x.key] = x.value
            else:
                pass
    time_a = time.time()

    sorted_tags = sorted(tag_counts, key = tag_counts.get, reverse=True)
    time_s = time.time()


    output = []

    for tag in sorted_tags:
        # if tag in mentalhealth_tags:
        count = tag_counts[tag]
        xx = {}
        xx[tag] = count
        output.append(xx)
    time_t = time.time()

    # output.append(time_q - time0)
    # output.append(time_a - time_q)
    # output.append(time_s - time_a)
    # output.append(time_t - time_s)

    return output



# @app.get("/twitter_tags/top_100")
# #@cache(expire=60*60*12)
# async def get_count():
#      query_result = db2.view('mydesigndoc/tag_count_map', group = True, reduce = True)
#      tag_counts = {}
#      for x in query_result:
#          tag_counts[x.key] = x.value
#      sorted_tags = sorted(tag_counts, key = tag_counts.get, reverse=True)

#      output = []

#      for tag in sorted_tags[:100]:
#          count = tag_counts[tag]
#          xx = {}
#          xx[tag] = count
#          output.append(xx)

#      return output



@app.get("/twitter_tags/top_10")
#@cache(expire=60*60*12)
async def get_count_3():
    time0 = time.time()
    query_result = db2.view('mydesigndoc/tag_count_map', group = True, reduce = True)
    time_q = time.time()
    tag_counts = {}
    for x in query_result:
        tag_counts[x.key] = x.value
    sorted_tags = sorted(tag_counts, key = tag_counts.get, reverse=True)
    time_s = time.time()


    output = []

    for tag in sorted_tags[:10]:
        count = tag_counts[tag]
        xx = {}
        xx[tag] = count
        output.append(xx)
    time_a = time.time()

    # output.append(time_q-time0)
    # output.append(time_s-time_q)
    # output.append(time_a-time_s)

    return output


@app.get("/twitter_tags/mentalhealth_about")
#@cache(expire=60*60*12)
async def get_count_4():
    time0 = time.time()
    tag_counts = {}

    for x in  mentalhealth_tags:
        query_result = db2.view('mydesigndoc/tag_count_map', group = True, reduce = True,  key = x, timeout = 5000)
        time_q = time.time()

        for x in query_result:
            if x.key in mentalhealth_tags:
                tag_counts[x.key] = x.value
            else:
                pass
    time_a = time.time()

    sorted_tags = sorted(tag_counts, key = tag_counts.get, reverse=True)
    time_s = time.time()


    output = []

    for tag in sorted_tags:
        # if tag in mentalhealth_tags:
        count = tag_counts[tag]
        xx = {}
        xx[tag] = count
        output.append(xx)
    time_t = time.time()

    # output.append(time_q - time0)
    # output.append(time_a - time_q)
    # output.append(time_s - time_a)
    # output.append(time_t - time_s)

    return output

@app.get("/twitter_tags/mentalhealth_about_2")
#@cache(expire=60*60*24*30)
async def get_count():
    time0 = time.time()
    tag_counts = {}

    for x in  mentalhealth_tags:
        query_result = db4.view('mydesigndoc/tag_count_map', group = True, reduce = True,  key = x)
        time_q = time.time()

        for x in query_result:
            if x.key in mentalhealth_tags:
                tag_counts[x.key] = x.value
            else:
                pass
    time_a = time.time()

    sorted_tags = sorted(tag_counts, key = tag_counts.get, reverse=True)
    time_s = time.time()


    output = []

    for tag in sorted_tags:
        # if tag in mentalhealth_tags:
        count = tag_counts[tag]
        xx = {}
        xx[tag] = count
        output.append(xx)
    time_t = time.time()

    # output.append(time_q - time0)
    # output.append(time_a - time_q)
    # output.append(time_s - time_a)
    # output.append(time_t - time_s)

    return output

@app.get("/twitter_tags/top_10_2")
#@cache(expire=60*60*24*30)
async def get_count():
    time0 = time.time()
    query_result = db4.view('mydesigndoc/tag_count_map', group = True, reduce = True)
    time_q = time.time()
    tag_counts = {}
    for x in query_result:
        tag_counts[x.key] = x.value
    sorted_tags = sorted(tag_counts, key = tag_counts.get, reverse=True)
    time_s = time.time()


    output = []

    for tag in sorted_tags[:10]:
        count = tag_counts[tag]
        xx = {}
        xx[tag] = count
        output.append(xx)
    time_a = time.time()

    # output.append(time_q-time0)
    # output.append(time_s-time_q)
    # output.append(time_a-time_s)

    return output
