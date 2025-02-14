package org.example;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;

import java.io.BufferedReader;
import java.io.FileReader;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.*;
import java.util.List;
import java.util.StringJoiner;


import static org.example.fileReader.readSQLFromFile;

public class DatabaseOperations {
    private static SqlSessionFactory sqlSessionFactory;
    public DatabaseOperations(SqlSessionFactory sqlSessionFactory) {
        this.sqlSessionFactory = sqlSessionFactory;
    }

    public void executeSQLFile(String sqlFilePath) {
        String sqlCommands = readSQLFromFile(sqlFilePath);

        // 分割SQL命令
        String[] commands = sqlCommands.split(";\\s*\\n");

        try (Connection conn = DBHelper.getConnection();
             Statement stmt = conn.createStatement()) {

            // 逐条执行SQL命令
            for (String command : commands) {
                if (!command.trim().isEmpty()) {
                    stmt.executeUpdate(command);
                }
            }

            System.out.println("SQL file executed successfully.");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }


    //使用Mybatis框架导入数据
    public void importCsv(String csvFilePath) {
        Path path = Paths.get(csvFilePath);
        String tableName = path.getFileName().toString().replaceFirst("[.][^.]+$", ""); // Remove file extension
        System.out.println("开始从CSV文件导入数据: " + csvFilePath + " 到表: " + tableName);

        List<String[]> records = fileReader.readCsv(csvFilePath);
        if (records.isEmpty()) {
            System.out.println("CSV文件没有数据，导入过程终止。");
            return;
        }

        String[] columnNames = records.get(0); // The first row contains column names
        List<String[]> dataRows = records.subList(1, records.size()); // Exclude the first row
        System.out.println("CSV文件读取完成，总计数据行数（不含表头）: " + dataRows.size());

        try (Connection conn = DBHelper.getConnection()) {
            String insertSql = generateInsertSQL(tableName, columnNames);
            insertData(conn, tableName, insertSql, dataRows);
            System.out.println("数据成功导入到表: " + tableName);
        } catch (Exception e) {
            System.err.println("导入CSV数据到数据库时发生错误: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private String generateInsertSQL(String tableName, String[] columnNames) {
        StringJoiner columns = new StringJoiner(", ", "(", ")");
        StringJoiner placeholders = new StringJoiner(", ", "(", ")");
        for (String columnName : columnNames) {
            columns.add(columnName);
            placeholders.add("?");
        }
        return "INSERT INTO " + tableName + " " + columns + " VALUES " + placeholders;
    }



    private void insertData(Connection conn, String tableName, String insertSql, List<String[]> dataRows) throws SQLException {
        try (PreparedStatement pstmt = conn.prepareStatement(insertSql)) {
            int columnsCount = pstmt.getParameterMetaData().getParameterCount();
            for (String[] rowData : dataRows) {
                for (int i = 0; i < columnsCount; i++) {
                    if (i < rowData.length && !rowData[i].isEmpty()) {
                        pstmt.setString(i + 1, rowData[i].trim());
                    } else {
                        pstmt.setNull(i + 1, Types.VARCHAR); // 允许数据库使用默认值
                    }
                }
                pstmt.addBatch();
            }
            pstmt.executeBatch(); // 执行批处理
        } catch (SQLException e) {
            e.printStackTrace();
            throw e; // 抛出异常供调用者处理
        }
    }

    public void importRoomCsv(String csvFilePath) {
        List<Room> rooms = fileReader.parseCsvToRooms(csvFilePath); // 假设这是一个将CSV解析为Room对象列表的方法
        try (SqlSession session = sqlSessionFactory.openSession()) {
            RoomMapper mapper = session.getMapper(RoomMapper.class);
            if (!rooms.isEmpty()) {
                mapper.insertRooms(rooms);
                session.commit();
                System.out.println("数据成功导入到表: room");
            } else {
                System.out.println("CSV文件没有数据，导入过程终止。");
            }
        } catch (Exception e) {
            System.err.println("导入CSV数据到数据库时发生错误: " + e.getMessage());
            e.printStackTrace();
        }
    }

    public void importStudentCsv(String csvFilePath) {
        List<Student> students = fileReader.parseCsvToStudents(csvFilePath); // 假设这是一个将CSV解析为Student对象列表的方法
        try (SqlSession session = sqlSessionFactory.openSession()) {
            StudentMapper mapper = session.getMapper(StudentMapper.class);
            if (!students.isEmpty()) {
                mapper.insertStudents(students); // 注意，这里假设您的StudentMapper接口中有一个insertStudents方法
                session.commit();
                System.out.println("数据成功导入到表: student");
            } else {
                System.out.println("CSV文件没有数据，导入过程终止。");
            }
        } catch (Exception e) {
            System.err.println("导入CSV数据到数据库时发生错误: " + e.getMessage());
            e.printStackTrace();
        }
    }




}
