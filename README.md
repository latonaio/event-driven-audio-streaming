# event-driven-audio-streaming  

何らかのイベントをトリガーとして、オーディオ配信を行うマイクロサービスです。   


### Clone and Build   
```
$ git clone git@bitbucket.org:latonaio/event-driven-audio-streaming.git
$ cd /path/to/event-driven-audio-streaming
$ make docker-build
```

### Create Table on MySQL  
```
CREATE TABLE audios (
  keyword VARCHAR(32) NOT NULL PRIMARY KEY,
  file_path VARCHAR(128) NOT NULL
);
INSERT INTO audios (keyword, file_path) values
  ("hello", "/var/lib/aion/Data/audios/hello.mp3")
;
```

### Edit Environment K8s Resource   
```
          env:
          - name: PORT
            value: "8888"
          - name: MYSQL_HOST
            value: "mysql"
          - name: MYSQL_PORT
            value: "3306"
          - name: MYSQL_USER
            value: <user>
          - name: MYSQL_PASSWORD
            value: <password>
          - name: MYSQL_DBNAME
            value: <dbname>
```

### How to Use   

* Access `ws://localhost:30102/websocket`
* Sending message specify keyword (like 'hello')
* Getting binary raw audio data until send 'EOS' message
* if keyword does not exist in Mysql, Getting 'Not found' message
