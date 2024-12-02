import cv2
import mediapipe as mp
import random

# MediaPipe 설정
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# 카메라 설정
cap = cv2.VideoCapture(0)

# 두더지 이미지 로드
mole_image = cv2.imread("snow.jpg", cv2.IMREAD_UNCHANGED)  # 두더지 이미지 경로

# 두더지 위치
mole_x, mole_y = random.randint(50, 500), random.randint(50, 500)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 영상 전처리
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # 두더지 이미지 크기 조정 (필요한 경우)
    mole_resized = cv2.resize(mole_image, (60, 60))  # 두더지 이미지 크기 조정

    # 두더지 이미지 투명도 채널 처리 (알파 채널이 있을 경우)
    if mole_resized.shape[2] == 4:  # 알파 채널이 있을 경우
        # ROI(Region of Interest) 지정
        roi = frame[mole_y:mole_y + mole_resized.shape[0], mole_x:mole_x + mole_resized.shape[1]]
        
        # 알파 채널 마스크를 사용하여 두더지 이미지를 화면에 합성
        img_bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mole_resized[:, :, 3]))
        img_fg = cv2.bitwise_and(mole_resized, mole_resized, mask=mole_resized[:, :, 3])
        frame[mole_y:mole_y + mole_resized.shape[0], mole_x:mole_x + mole_resized.shape[1]] = cv2.add(img_bg, img_fg)
    else:
        # 알파 채널이 없을 경우 그냥 합성
        frame[mole_y:mole_y + mole_resized.shape[0], mole_x:mole_x + mole_resized.shape[1]] = mole_resized

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 손의 Landmark와 두더지 위치 비교
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # 두더지와 가까운지 확인
                if abs(cx - mole_x) < 30 and abs(cy - mole_y) < 30:
                    print("Mole hit!")
                    mole_x, mole_y = random.randint(50, 500), random.randint(50, 500)  # 두더지 위치 재설정

    # 결과 출력
    cv2.imshow("Dudu Game", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC로 종료
        break

cap.release()
cv2.destroyAllWindows()
