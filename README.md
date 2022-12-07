#API Documentation

##Using Time Series To get All data

Get all the data coming from a specific time series

**URL** : `/data/time`

**Method** : `GET`

**Data constraints**

```json
{
    "start": "[valid date time format start time]",
    "end": "[valid date time format end time]"
}
```

**Data example**

```json
    [
		{
			"_id": {
				"$oid": "638ee3f7703e0f92293097c7"
			},
			"action": "unlocked",
			"customerid": "83ed12c6-75ec-11ed-a1eb-0242ac120002",
			"location": "back-door",
			"timestamp": {
				"$date": "2022-12-06T01:40:55Z"
			}
		}
	]

```

##Using Time Series To get All data From Certain Customer

Get all the data coming from a specific time series from a specific customer

**URL** : `/data/time/customerid`

**Method** : `GET`

**Data constraints**
```json
{
    "start": "[valid date time format start time]",
    "end": "[valid date time format end time]",
	"customerid": "[valid customer uuid]"
}
```

**Data example**
```json
    [
		{
			"_id": {
				"$oid": "638ee3f7703e0f92293097c7"
			},
			"action": "unlocked",
			"customerid": "83ed12c6-75ec-11ed-a1eb-0242ac120002",
			"location": "back-door",
			"timestamp": {
				"$date": "2022-12-06T01:40:55Z"
			}
		}
	]

```

##Using Time Series To get All data From Customer Specific Location

Get all the data coming from a specific time series from a specific customer and a specific location

**URL** : `/data/time/customerid/location`

**Method** : `GET`

**Data constraints**
```json
{
    "start": "[valid date time format start time]",
    "end": "[valid date time format end time]",
	"customerid": "[valid customer uuid]"
	"location": "[valid location of customer device]"
}
```

**Data example**
```json
    [
		{
			"_id": {
				"$oid": "638ee3f7703e0f92293097c7"
			},
			"action": "unlocked",
			"customerid": "83ed12c6-75ec-11ed-a1eb-0242ac120002",
			"location": "back-door",
			"timestamp": {
				"$date": "2022-12-06T01:40:55Z"
			}
		}
	]

```

##Getting all data

Get all data from all customers and devices

**URL** : `/data`

**Method** : `GET`

**Data example**
```json
    [
		{
			"_id": {
				"$oid": "638ee3f7703e0f92293097c7"
			},
			"action": "unlocked",
			"customerid": "83ed12c6-75ec-11ed-a1eb-0242ac120002",
			"location": "back-door",
			"timestamp": {
				"$date": "2022-12-06T01:40:55Z"
			}
		}
	]

```

##Getting all data

Get all data from all customers and devices

**URL** : `/data`

**Method** : `GET`

**Data example**
```json
    [
		{
			"_id": {
				"$oid": "638ee3f7703e0f92293097c7"
			},
			"action": "unlocked",
			"customerid": "83ed12c6-75ec-11ed-a1eb-0242ac120002",
			"location": "back-door",
			"timestamp": {
				"$date": "2022-12-06T01:40:55Z"
			}
		}
	]

```

##Getting all locked devices

Get all currently locked devices

**URL** : `/data/locked`

**Method** : `GET`

**Data example**
```json
    [
		{
			"_id": {
				"$oid": "638ee3f7703e0f92293097c7"
			},
			"action": "locked",
			"customerid": "83ed12c6-75ec-11ed-a1eb-0242ac120002",
			"location": "back-door",
			"timestamp": {
				"$date": "2022-12-06T01:40:55Z"
			}
		}
	]

```

##Getting all unlocked devices

Get all unlocked device from mongo

**URL** : `/data/unlocked`

**Method** : `GET`

**Data example**
```json
    [
		{
			"_id": {
				"$oid": "638ee3f7703e0f92293097c7"
			},
			"action": "unlocked",
			"customerid": "83ed12c6-75ec-11ed-a1eb-0242ac120002",
			"location": "back-door",
			"timestamp": {
				"$date": "2022-12-06T01:40:55Z"
			}
		}
	]

```


##Getting all devices from specific location

Get all devices from a specific location

**URL** : `/data/location/<desired-location>`

**Method** : `GET`

**Data example**
```json
    [
		{
			"_id": {
				"$oid": "638ee3f7703e0f92293097c7"
			},
			"action": "unlocked",
			"customerid": "83ed12c6-75ec-11ed-a1eb-0242ac120002",
			"location": "back-door",
			"timestamp": {
				"$date": "2022-12-06T01:40:55Z"
			}
		}
	]

```

##Getting all devices from specific user

Get all devices from specific user

**URL** : `/data/location/<desired-user>`

**Method** : `GET`

**Data example**
```json
    [
		{
			"_id": {
				"$oid": "638ee3f7703e0f92293097c7"
			},
			"action": "unlocked",
			"customerid": "83ed12c6-75ec-11ed-a1eb-0242ac120002",
			"location": "back-door",
			"timestamp": {
				"$date": "2022-12-06T01:40:55Z"
			}
		}
	]

```

##Posting a new action

Add new action to Mongo

**URL** : `/data`

**Method** : `POST`

**Data constraints**
```json
{
    "action":"[locked or unlocked]",
    "location": "[device location name]",
    "userid":"[valid user uuid]"
}
```

**Data example**
```json
    {
		"data saved": "back-door was unlocked by 83ed12c6-75ec-11ed-a1eb-0242ac120002"
	}
```

##Deleting a log

Delete log from mongo

**URL** : `/data`

**Method** : `DELETE`

**Data constraints**
```json
{
    "userid":"[valid mongo object id]"
}
```

**Data example**
```json
{
    "83ed12c6-75ec-11ed-a1eb-0242ac120002": "successfully deleted"
}
```

##Replacing a log

Replace fields from current log

**URL** : `/data`

**Method** : `PUT`

**Data constraints**
```json
{
    "action":"[locked or unlocked]",
    "location": "[device location name]",
    "userid":"[valid user uuid]"
}
```

**Data example**
```json
{
    "638ee1472c2bf55725671a8c": "was updated"
}
```