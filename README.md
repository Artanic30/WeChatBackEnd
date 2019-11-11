# WeChatBackEnd

## API

### For All Members

#### Login
Supported method:  `POST`

Registered at `/absence/login/`

```json
{
    "name": "David",
    "union_id": "aljsd8asdabsdb728d1djhasbkdjb"
}
```

#### Abesence Application 
Supported method:  `POST`

Registered at `/absence/`

```json
{
    "reason": "reasons",
    "time": "2018-01-22T09:12:43.083Z",
    "name": "David"
}
```

#### Abesence Information
Supported method:  `GET`

Registered at `/absence/`

```json
[
    {
        "id": 1,
        "applier": "David",
        "processor": null,
        "reason": "testReason",
        "time_absence": "2019-11-10",
        "time_apply": "2019-11-10",
        "result": "Not processed yet!",
        "permission": false
    }
]
```


### For Managers

#### All Absence Information 
Supported method:  `GET`

Registered at `/manage/`

```json
[
    {
        "id": 4,
        "applier": "David",
        "processor": null,
        "reason": "testReason",
        "time_absence": "2019-11-10",
        "time_apply": "2019-11-10",
        "result": "Not processed yet!",
        "permission": false
    }
]
```

#### All Absence Information 
Supported method:  `POST`

Registered at `/manage/<int:pk>/process/`   
pk is the pk of absence, transform in form-data instead of application/json

```json
  {
    "result": "Reason for allowing/not allowing absence",
    "is_prove": false,
    "approver_name": "David"
  }
```

#### Members Absent
Supported method:  `GET`

Registered at `/manager/<str:time>/present/`
time in YYYY-MM-DD formate

```json
{
  "time": "2018-01-22T09:12:43.083Z",
  "members":[
    {
        "name": "David",
        "state": "absent"
    },
    {
        "name": "John",
        "state": "absent"
    }
  ]
}
```

