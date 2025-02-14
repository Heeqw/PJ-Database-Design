package org.example;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        DatabaseOperations operations= new DatabaseOperations(MybatisUtil.getSqlSessionFactory());

        String csvFilePath1 = "D:\\大学\\大二下\\数据库\\lab\\lab1\\lab1数据\\room.csv";
        String csvFilePath2 = "D:\\大学\\大二下\\数据库\\lab\\lab1\\lab1数据\\student.csv";

//        String createSqlFilePath1 = "D:\\softwareEngineering\\dataBaseSystem\\lab1\\src\\main\\java\\org\\example\\table_create.sql";
//        String createSqlFilePath2 = "D:\\softwareEngineering\\dataBaseSystem\\lab1\\src\\main\\java\\org\\example\\student_create.sql";
        String createSQLfilePath = "D:\\softwareEngineering\\dataBaseSystem\\lab1\\src\\main\\java\\org\\example\\createTable.sql";

//        String removeDuplicateSqlPath = "D:\\softwareEngineering\\dataBaseSystem\\lab1\\src\\main\\java\\org\\example\\delete_Duplicate.sql";

//        operations.executeSQLFile(createSqlFilePath1);
//        operations.executeSQLFile(createSqlFilePath2);
        operations.executeSQLFile(createSQLfilePath);

        operations.importCsv(csvFilePath1);
        operations.importCsv(csvFilePath2);

//        operations.executeSQLFile(removeDuplicateSqlPath);
    }
}