package org.example;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;
public class fileReader {
    public static List<String[]> readCsv(String filepath){
        List<String[]> records = new ArrayList<>();
        try(BufferedReader br = new BufferedReader(new FileReader(filepath))){
            String line;
            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");
                for (int i = 0; i < values.length; i++) {
                    // 去除每个值周围的双引号
                    values[i] = values[i].trim().replace("\"", "");
                }
                records.add(values);
            }
        }catch (Exception e){
            e.printStackTrace();
        }
        return records;
    }

    public static String readSQLFromFile(String filePath) {
        StringBuilder sql = new StringBuilder();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                sql.append(line).append(System.lineSeparator()); // 将每一行添加到StringBuilder中
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return sql.toString(); // 将StringBuilder转换为String并返回
    }

    public static List<Room> parseCsvToRooms(String filepath) {
        List<String[]> records = fileReader.readCsv(filepath);
        List<Room> rooms = new ArrayList<>();
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"); // 根据您的实际日期格式调整
        for (String[] record : records.subList(1, records.size())) { // 跳过标题行
            Room room = new Room();
            room.setKdno(record[0]);
            room.setKcno(record[1]);
            room.setCcno(record[2]);
            room.setKdname(record[3]);
            try {
                room.setExptime(dateFormat.parse(record[4]));
            } catch (Exception e) {
                e.printStackTrace();
            }
            room.setPapername(record.length > 5 ? record[5] : null); // 处理可能的空值
            rooms.add(room);
        }
        return rooms;
    }

    public static List<Student> parseCsvToStudents(String filepath) {
        List<String[]> records = fileReader.readCsv(filepath);
        List<Student> students = new ArrayList<>();
        for (String[] record : records.subList(1, records.size())) { // 跳过标题行
            Student student = new Student();
            student.setRegistno(record[0]);
            student.setName(record[1]);
            student.setKdno(record[2]);
            student.setKcno(record[3]);
            student.setCcno(record[4]);
            student.setSeat(Integer.parseInt(record[5])); // 假设seat总是有效的整数
            students.add(student);
        }
        return students;
    }

}
