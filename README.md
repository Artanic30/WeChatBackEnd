# WeChatBackEnd

## API

###For Members

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
    "reason": "reasons",
    "time": "2018-01-22T09:12:43.083Z",
    "name": "David"
  }
]
```


#### Members Present 
Supported method:  `GET`

Registered at `/manager/<str:time>/present/`   time in YYYY-MM-DD formate

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
        "state": "present"
    }
  ]
}
```


###For Managers

#### All Absence Information 
Supported method:  `GET`

Registered at `/manage/`

```json
[
  {
    "pk": 5,
    "name": "David",
    "reason": "reasons",
    "time": "2018-01-22T09:12:43.083Z"
  }
]
```

#### All Absence Information 
Supported method:  `POST`

Registered at `/manage/<int:pk>/`

```json
  {
    "pk": 5,
    "result": "Reason for allowing/not allowing absence",
    "is_prove": false
  }
```

