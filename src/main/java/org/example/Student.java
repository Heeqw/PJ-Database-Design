package org.example;

public class Student {
    private String registno;
    private String name;
    private String kdno;
    private String kcno;
    private String ccno;
    private int seat;

    // 构造函数
    public Student() {
    }

    public Student(String registno, String name, String kdno, String kcno, String ccno, int seat) {
        this.registno = registno;
        this.name = name;
        this.kdno = kdno;
        this.kcno = kcno;
        this.ccno = ccno;
        this.seat = seat;
    }

    // Getter和Setter
    public String getRegistno() {
        return registno;
    }

    public void setRegistno(String registno) {
        this.registno = registno;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getKdno() {
        return kdno;
    }

    public void setKdno(String kdno) {
        this.kdno = kdno;
    }

    public String getKcno() {
        return kcno;
    }

    public void setKcno(String kcno) {
        this.kcno = kcno;
    }

    public String getCcno() {
        return ccno;
    }

    public void setCcno(String ccno) {
        this.ccno = ccno;
    }

    public int getSeat() {
        return seat;
    }

    public void setSeat(int seat) {
        this.seat = seat;
    }

    // toString() 方法，可选，用于打印对象信息
    @Override
    public String toString() {
        return "Student{" +
                "registno='" + registno + '\'' +
                ", name='" + name + '\'' +
                ", kdno='" + kdno + '\'' +
                ", kcno='" + kcno + '\'' +
                ", ccno='" + ccno + '\'' +
                ", seat=" + seat +
                '}';
    }
}
