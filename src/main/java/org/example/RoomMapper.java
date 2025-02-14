package org.example;

import org.apache.ibatis.annotations.Param;
import java.util.List;

public interface RoomMapper {
    void insertRooms(@Param("rooms") List<Room> rooms);
}
