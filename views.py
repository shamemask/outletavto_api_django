from django.shortcuts import render
from .api_client import Pr_Lg, RosskoAPI, ABCP
import pandas as pd
from tabulate import tabulate
import json

async def ABCP_table(request, endpoint):
    args_req = request.GET
    context = await ABCP().get_pd(endpoint, **args_req)
    return render(request, 'mainapp\\dftable.html', context)

async def Pr_Lg_table(request, endpoint):
    args = request.GET
    context = await Pr_Lg().get_pd(endpoint, **args)
    return render(request, 'mainapp\\dftable.html', context)


async def Rossko_table(request, endpoint):
    args = request.GET
    context = await RosskoAPI(endpoint).get_pd(endpoint,**args)
    return render(request, 'mainapp\\dftable.html', context)