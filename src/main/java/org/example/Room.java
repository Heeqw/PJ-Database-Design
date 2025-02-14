package org.example;

import java.util.Date;

public class Room {
    private String kdno;
    private String kcno;
    private String ccno;
    private String kdname;
    private Date exptime; // 假设使用java.util.Date，根据实际情况调整
    private String papername; // 可以为空

    public Room(){
    }

    public Room(String kdno,String kcno,String ccno,String kdname,Date exptime,String papername){
        this.kdno = kdno;
        this.kcno = kcno;
        this.ccno = ccno;
        this.kdname = kdname;
        this.exptime = exptime;
        this.papername = papername;
    }

    public void setKdno(String kdno){
        this.kdno = kdno;
    }

    public void setKcno(String kcno){
        this.kcno = kcno;
    }

    public void setCcno(String ccno){
        this.ccno = ccno;
    }

    public void setExptime(Date exptime){
        this.exptime = exptime;
    }

    public void setKdname(String kdname){
        this.kdname = kdname;
    }

    public void setPapername(String papername){
        this.papername = papername;
    }
}

