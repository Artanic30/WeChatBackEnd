# WeChatBackEnd

## API

### For All Members

#### Login
Supported method:  `POST`

Registered at `/account/login/`

```json
{
    "name": "David",
    "app_id": "aljsd8asdabsdb728d1djhasbkdjb",
    "app_secret": "dasdasdasdabsdb728d1djhasbkdjb",
    "code": "sdasdasdasda"
}
```
return value

```
{
    "msg": "login!",
    "token": "kjdagsjhdkanbcajgscjdgajhsbcjhagsc"
}
```
to remain login state, add followering to your request header
```
header: {
    'Authorization': 'JWT <str:token>'
}
example:

header: {
    'Authorization': 'JWT lakshdkjagsdjkgaskjdgkjasgdkjakjabsdkjasd'
}

```
Ever since the first login, one wechat union id will be bound with a name in the 
member name list.
If login fail, the backend will retrun
```json
{
    "msg": "Error information"
}
```
and you may show the message directly to user

#### Abesence Application 
Supported method:  `POST`

Registered at `/absence/`

```json
{
    "reason": "reasons",
    "time_absence": "2018-01-22",
    "type": "全体排练"
}
```
error response
```json
{
    "msg": "error reasons"
}
```
type choices: 全体排练, 弦乐分排, 管乐分排, 弦乐重奏, 管乐重奏, 全体排练+弦乐分排, 全体排练+管乐分排
times reach upper bound
```json
{
    "msg": "You have used up all of your chances."
}
```

#### Change Abesence Application 
Supported method:  `PUT`

Registered at `/absence/<int:absence_id>/`

```json
{
    "reason": "reasons",
    "time_absence": "2018-01-22",
    "type": "A"
}
```
type choices: 全体排练, 弦乐分排, 管乐分排, 弦乐重奏, 管乐重奏, 全体排练+弦乐分排, 全体排练+管乐分排

#### Delete Abesence Application 
Supported method:  `DELETE`

Registered at `/absence/<int:absence_id>/`

```json
401 status code
no return data
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
        "permission": false,
        "type": "全体"
    }
]
```


### For Managers

any student try access these information will get code 401

#### All Absence Information 
Supported method:  `GET`

Registered at `/manager/`

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
        "permission": false,
        "type": "全体"
    }
]
```

#### All Absence Information 
Supported method:  `PUT`

Registered at `/manager/<int:absence_id>/`   
id is the pk of absence

```json
  {
    "processor": "David"
    "result": "Reason for allowing/not allowing absence",
    "permission": false
  }
```

return data

```json
  {
    "msg": "xxxxxxxx"
  }
```

#### Members Absent
Supported method:  `GET`

Registered at `/manager/<str:time>/present/`
time in YYYY-MM-DD formate example: ('2020-3-12')

```json
{
  "time": "2018-01-22",
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

#### Members Absent in Next Rehearsal
filtered by the closest time anyone applied for absence.

Supported method:  `GET`

Registered at `/manager/next/`

```json
{
    "time": "2020-03-24",
    "stringed": [
        {
            "id": 23340,
            "applier": "赵乘风",
            "processor": null,
            "reason": "test2",
            "time_absence": "2020-03-24",
            "type": "全体排练",
            "time_apply": "2020-02-08",
            "result": "Not processed yet!",
            "permission": false
        }
    ]
    "wind": [
       {
            "id": 23340,
            "applier": "赵乘风",
            "processor": null,
            "reason": "test2",
            "time_absence": "2020-03-24",
            "type": "全体排练",
            "time_apply": "2020-02-08",
            "result": "Not processed yet!",
            "permission": false
        }
    ],
    "percussion": [
          {
            "id": 23340,
            "applier": "赵乘风",
            "processor": null,
            "reason": "test2",
            "time_absence": "2020-03-24",
            "type": "全体排练",
            "time_apply": "2020-02-08",
            "result": "Not processed yet!",
            "permission": false
        }
    ],
}
```

#### Members Absent Before the Current Date 

Supported method:  `GET`

Registered at `/manager/history/`

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
        "permission": false,
        "type": "全体"
    }
]
```

#### Members Absent After the Current Date 

Supported method:  `GET`

Registered at `/manager/future/`

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
        "permission": false,
        "type": "全体"
    }
]
```

## Depoly(Only the part I remember)

# start virtual environment
cd /<env:root_dir>
source bin/activate

# install requirement library
pip3 install -r requirements.txt

tips: (sudo pip3 install -r requirements.txt) will install teh library to the system's environment instead of env's

# update database(abandoned, merged into script)
python3 manage.py makemigrations
python3 manage.py migrate

# start uwsgi 
sudo bash update.sh (the script is set up)
