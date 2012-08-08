#!/usr/bin/env python

from SimpleSeer.base import *
from SimpleSeer.Session import Session
from os import system

if (len(sys.argv) > 1):
   config_file = sys.argv[1] 
else:
   config_file = "./simpleseer.cfg"

Session(config_file)

from SimpleSeer.models.Inspection import Inspection
from SimpleSeer.models.Inspection import Measurement 
from SimpleSeer.models.OLAP import OLAP 
from SimpleSeer.models.Chart import Chart
 

system('echo "db.dropDatabase()" | mongo default')




insp = Inspection( name= "Motion", method="motion")
insp.save()

meas = Measurement( name="movement", label="Movement", method = "movement", parameters = dict(), units = "", featurecriteria = dict( index = 0 ), inspection = insp.id )
meas.save()


## Delivery time
o = OLAP()
o.name = 'Movement'  
o.maxLen = 1000 
o.olapFilter = [{'type': 'measurement', 'name': 'movement.numeric', 'exists': True}]
o.since = None
o.before = None
o.customFilter = {} 
o.statsInfo = []
o.save()

c = Chart()
c.name = 'Movement'
c.olap = o.name
c.style = 'spline'
c.minval = 0
c.maxval = None
c.xtype = 'datetime'
c.colormap = {}
c.labelmap = {}
c.accumulate = False
c.renderorder = 1
c.halfsize = False
c.realtime = True
c.dataMap = ['capturetime','movement.numeric']
c.metaMap = ['movement.measurement_id', 'movement.inspection_id', 'id']
c.save()

## Delivery time, moving average
o1 = OLAP()
o1.name = 'Movement MA'  
o1.maxLen = 1000 
o.olapFilter = [{'type': 'measurement', 'name': 'movement.numeric', 'exists': True}]
o1.queryType = 'measurement_id' 
o1.queryId = meas.id 
o1.since = None
o1.before = None
o1.customFilter = {} 
o1.statsInfo = [{'field': 'movement.numeric', 'fn': 'rolling_mean', 'param': 5}]
o1.save()

c1 = Chart()
c1.name = 'Movement, 5 Period Moving Average'
c1.olap = o1.name
c1.style = 'spline'
c1.minval = 0
c1.maxval = None
c1.xtype = 'datetime'
c1.colormap = {}
c1.labelmap = {}
c1.accumulate = False
c1.renderorder = 1
c1.halfsize = False
c1.realtime = True
c1.dataMap = ['capturetime','movement.numeric', 'movement.numeric.rolling_mean']
c1.metaMap = ['movement.measurement_id', 'movement.inspection_id', 'id']
c1.save()
