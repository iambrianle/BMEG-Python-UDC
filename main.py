import pandas as pd
import math
import matplotlib.pyplot as plt


# load the Excel file and clean the file
file_path = 'motiondata.xlsx'
sheet_name = 'S2' 

df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=2)
df.columns = df.columns.str.strip()

# columns for right and left side markers
right_hip_cols = ["'XRxAsis  '", "'YRxAsis  '", "'ZRxAsis  '"]
right_knee_cols = ["'XRxLatCon'", "'YRxLatCon'", "'ZRxLatCon'"]
right_ankle_cols = ["'XRxLatMal'", "'YRxLatMal'", "'ZRxLatMal'"]

left_hip_cols = ["'XLxAsis  '", "'YLxAsis  '", "'ZLxAsis  '"]
left_knee_cols = ["'XLxLatCon'", "'YLxLatCon'", "'ZLxLatCon'"]
left_ankle_cols = ["'XLxLatMal'", "'YLxLatMal'", "'ZLxLatMal'"]

# columns for head, neck, and torso
head_cols = ["'XRxCheec '", "'YRxCheec '", "'ZRxCheec '"]
neck_cols = ["'XC7      '", "'YC7      '", "'ZC7      '"]
torso_cols = ["'Xmaxkif  '", "'Ymaxkif  '", "'Zmaxkif  '"]

# toe markers
right_foot_cols = ["'XRxToe1  '", "'YRxToe1  '", "'ZRxToe1  '"]
left_foot_cols = ["'XLxToe1  '", "'YLxToe1  '", "'ZLxToe1  '"]

# movement marker
movement_marker_cols = ["'Xmaxkif  '", "'Ymaxkif  '", "'Zmaxkif  '"]


# extract the data
right_hip = df[right_hip_cols].iloc[1:].astype(float).to_numpy()
right_knee = df[right_knee_cols].iloc[1:].astype(float).to_numpy()
right_ankle = df[right_ankle_cols].iloc[1:].astype(float).to_numpy()
right_foot = df[right_foot_cols].iloc[1:].astype(float).to_numpy()
left_hip = df[left_hip_cols].iloc[1:].astype(float).to_numpy()
left_knee = df[left_knee_cols].iloc[1:].astype(float).to_numpy()
left_ankle = df[left_ankle_cols].iloc[1:].astype(float).to_numpy()
left_foot = df[left_foot_cols].iloc[1:].astype(float).to_numpy()
head = df[head_cols].iloc[1:].astype(float).to_numpy()
neck = df[neck_cols].iloc[1:].astype(float).to_numpy()
torso = df[torso_cols].iloc[1:].astype(float).to_numpy()
movement = df[movement_marker_cols].iloc[1:].astype(float).to_numpy()


# Convert time column to numeric
time = pd.to_numeric(df['Marker Name'][1:])

# calculate distance between two 3D points
def calculate_distance(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    z_diff = p2[2] - p1[2]
    return math.sqrt(x_diff ** 2 + y_diff ** 2 + z_diff ** 2)

# calculate angle based on cosine
def calculate_angle(a, b, c, epsilon=1e-8):
    if b < epsilon or c < epsilon:
        return 0.0

    cos_theta = (b**2 + c**2 - a**2) / (2 * b * c)
    cos_theta = max(min(cos_theta, 1.0), -1.0)

    theta_radians = math.acos(cos_theta)
    return math.degrees(theta_radians)

# calculate angle at a joint given the positions of the points
def calculate_angle_between_points(p1, p2, p3):
    a = calculate_distance(p1, p2)
    b = calculate_distance(p2, p3)
    c = calculate_distance(p1, p3)
    return calculate_angle(a, b, c)

# calculate walking speed using movement data
def calculate_walking_speed(start, end, final_time):
    distance = calculate_distance(start, end)
    speed = distance / final_time
    return speed


start = tuple(float(x) for x in movement[0])
end = tuple(float(x) for x in movement[-1])
final_time = float(time.iloc[-1])
walking_speed_result = calculate_walking_speed(start, end, final_time)
print(f"Walking speed: {walking_speed_result:.2f} meters per second")


def KneeAngleRight(hip, knee, ankle):
    return calculate_angle_between_points(hip, knee, ankle)

def KneeAngleLeft(hip, knee, ankle):
    return calculate_angle_between_points(hip, knee, ankle)

def AnkleAngleRight(knee, ankle, foot):
    return calculate_angle_between_points(knee, ankle, foot)

def AnkleAngleLeft(knee, ankle, foot):
    return calculate_angle_between_points(knee, ankle, foot)

def HeadNeckAngle(head, neck, torso):
    return calculate_angle_between_points(head, neck, torso)

# angles over time using the functions created
knee_angles_right = [KneeAngleRight(rh, rk, ra) for rh, rk, ra in zip(right_hip, right_knee, right_ankle)]
knee_angles_left = [KneeAngleLeft(lh, lk, la) for lh, lk, la in zip(left_hip, left_knee, left_ankle)]
ankle_angles_right = [AnkleAngleRight(rk, ra, rf) for rk, ra, rf in zip(right_knee, right_ankle, right_foot)]
ankle_angles_left = [AnkleAngleLeft(lk, la, lf) for lk, la, lf in zip(left_knee, left_ankle, left_foot)]
head_neck_angles = [HeadNeckAngle(h, n, t) for h, n, t in zip(head, neck, torso)]


# Plot data
plt.figure(figsize=(12, 8))
plt.plot(time, knee_angles_right, label='Right Knee Angle', marker= 'o', color='orange')
plt.plot(time, knee_angles_left, label='Left Knee Angle', marker='o', color='blue')
plt.plot(time, ankle_angles_right, label='Right Ankle Angle', marker='o', color='green')
plt.plot(time, ankle_angles_left, label='Left Ankle Angle', marker='o', color='red')
plt.plot(time, head_neck_angles, label='Head/Neck Angle', marker='o', color='purple')
plt.title(f'Angle Profiles Over Time for {sheet_name}')
plt.xlabel('Time (seconds)')
plt.ylabel('Angle (degrees)')
plt.legend()
plt.grid(True)
plt.show()