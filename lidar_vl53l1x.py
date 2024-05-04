import serial

LIDAR_MODULE_NUMBER = 16
LIDAR_FRAME_SIZE = 114

# Finite State Machine
class AresLidarParsingStatus:
    BEGIN = 0
    INFO = 1
    DISTANCE_MES = 2

# Lidar class (Have the same role than a C structure)
class AresLidar:
    def __init__(self):
        self.parsing_status = AresLidarParsingStatus.BEGIN
        self.active_sensor = 0
        self.ROI_number = 0
        self.measure_number = 0
        self.rx_storage = bytearray(LIDAR_FRAME_SIZE * 2)
        self.measure = [[0, 0] for _ in range(LIDAR_MODULE_NUMBER)]

# Function to retrieve LidarDistance data
def get_lidar_data(lidar):
    reading_head = 0
    wait_for_head_cmp = 0
    wait_for_fill = 0

    while reading_head < len(lidar.rx_storage):
        reading_head_limit = len(lidar.rx_storage) if reading_head < LIDAR_FRAME_SIZE else LIDAR_FRAME_SIZE

        while reading_head < reading_head_limit:
            if lidar.parsing_status == AresLidarParsingStatus.BEGIN:
                if lidar.rx_storage[reading_head] == 0xFF:
                    wait_for_head_cmp += 1
                else:
                    wait_for_head_cmp = 0

                if wait_for_head_cmp > 5:
                    wait_for_head_cmp = 0
                    lidar.parsing_status = AresLidarParsingStatus.INFO

            elif lidar.parsing_status == AresLidarParsingStatus.INFO:
                if wait_for_head_cmp == 0:
                    lidar.active_sensor = lidar.rx_storage[reading_head]
                    wait_for_head_cmp += 1
                elif wait_for_head_cmp == 1:
                    lidar.ROI_number = lidar.rx_storage[reading_head]
                    wait_for_head_cmp += 1
                elif wait_for_head_cmp > 1:
                    lidar.measure_number = lidar.rx_storage[reading_head]
                    wait_for_head_cmp = 0
                    lidar.parsing_status = AresLidarParsingStatus.DISTANCE_MES

            elif lidar.parsing_status == AresLidarParsingStatus.DISTANCE_MES:
                if wait_for_fill % 3 == 0 and wait_for_head_cmp < lidar.measure_number:
                    lidar.measure[wait_for_head_cmp][0] = lidar.rx_storage[reading_head]
                    wait_for_fill += 1
                elif wait_for_fill % 3 == 1 and wait_for_head_cmp < lidar.measure_number:
                    lidar.measure[wait_for_head_cmp][1] = lidar.rx_storage[reading_head]
                    lidar.measure[wait_for_head_cmp][1] <<= 8
                    wait_for_fill += 1
                elif wait_for_fill % 3 == 2 and wait_for_head_cmp < lidar.measure_number:
                    lidar.measure[wait_for_head_cmp][1] += lidar.rx_storage[reading_head]
                    wait_for_fill += 1
                    wait_for_head_cmp += 1

                if wait_for_head_cmp >= lidar.measure_number:
                    wait_for_fill = 0
                    wait_for_head_cmp = 0
                    lidar.parsing_status = AresLidarParsingStatus.BEGIN

            reading_head += 1
        if reading_head >= LIDAR_FRAME_SIZE:
            reading_head_limit = LIDAR_FRAME_SIZE

    return lidar

def main():
    # Open serial communication
    ser = serial.Serial("/dev/ttyAMA1", baudrate=115200, timeout=5.0)
    print("Serial port:", ser.name)
    ser.flush()

    while True:
        lidar_data = AresLidar()
        lidar_data.rx_storage = ser.read(LIDAR_FRAME_SIZE * 2)
        processed_data = get_lidar_data(lidar_data)
        distances = [distance[1] for distance in processed_data.measure]
        min_distance = min(distances)

        # Distance threshold
        stop_threshold = 450

        robot_speed = 0.0

        # The '20' condition is to prevent data jumps
        if 20 <= min_distance <= stop_threshold:
            robot_speed = 0.0
        else:
            robot_speed = 1.0

        # Displaying data
        print("Robot Speed:", robot_speed)

if __name__ == '__main__':
    main()
