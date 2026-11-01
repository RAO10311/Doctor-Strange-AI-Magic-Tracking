import cv2
import mediapipe as mp
import numpy as np
import math
import random
from collections import deque

W, H = 1280, 720
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
trails = {}
particles = []

def glow_circle(frame, center, radius, tick, color=(35, 150, 255)):
    overlay = frame.copy()
    cx, cy = center
    for r in (radius, int(radius * .83), int(radius * .57)):
        cv2.circle(overlay, (cx, cy), r, color, 2, cv2.LINE_AA)
    for i in range(36):
        a = 2 * math.pi * i / 36 + tick * .025
        inner = radius * (.72 if i % 3 == 0 else .86)
        outer = radius * (.94 if i % 3 == 0 else 1.0)
        p1 = (int(cx + inner * math.cos(a)), int(cy + inner * math.sin(a)))
        p2 = (int(cx + outer * math.cos(a)), int(cy + outer * math.sin(a)))
        cv2.line(overlay, p1, p2, color, 2, cv2.LINE_AA)
    cv2.ellipse(overlay, (cx, cy), (int(radius * .42), int(radius * .42)),
                int((tick * 5) % 360), 0, 245, (100, 205, 255), 3, cv2.LINE_AA)
    overlay = cv2.GaussianBlur(overlay, (0, 0), 7)
    frame[:] = cv2.addWeighted(frame, 1.0, overlay, .62, 0)
    cv2.circle(frame, center, radius, (170, 225, 255), 1, cv2.LINE_AA)

def glow_line(frame, p1, p2):
    overlay = frame.copy()
    cv2.line(overlay, p1, p2, (20, 145, 255), 13, cv2.LINE_AA)
    overlay = cv2.GaussianBlur(overlay, (0, 0), 8)
    frame[:] = cv2.addWeighted(frame, 1.0, overlay, .65, 0)
    cv2.line(frame, p1, p2, (190, 235, 255), 3, cv2.LINE_AA)

def fingers_up(hand):
    lm = hand.landmark
    return [lm[t].y < lm[p].y for t, p in zip((8, 12, 16, 20), (6, 10, 14, 18))]

def add_particles(center, count=3):
    cx, cy = center
    for _ in range(count):
        angle = random.random() * math.tau
        speed = random.uniform(1.0, 4.0)
        particles.append([float(cx), float(cy), math.cos(angle) * speed,
                          math.sin(angle) * speed, random.randint(14, 30)])

def update_particles(frame):
    alive = []
    for p in particles:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
        if p[4] > 0:
            cv2.circle(frame, (int(p[0]), int(p[1])), 2, (90, 190, 255), -1, cv2.LINE_AA)
            alive.append(p)
    particles[:] = alive

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam not found. Check Windows camera permissions.")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
    tick = 0

    with mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                        model_complexity=1, min_detection_confidence=.65,
                        min_tracking_confidence=.6) as hands:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            tick += 1
            status = "Show your hand to cast a spell"

            if result.multi_hand_landmarks:
                for idx, hand in enumerate(result.multi_hand_landmarks):
                    lm = hand.landmark
                    up = fingers_up(hand)
                    palm = (int(lm[9].x * w), int(lm[9].y * h))
                    tip = (int(lm[8].x * w), int(lm[8].y * h))
                    mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
                    if all(up):
                        glow_circle(frame, palm, 112, tick + idx * 25)
                        add_particles(palm, 2)
                        status = "MAGIC SHIELD | OPEN PALM"
                        trails.pop(idx, None)
                    elif up[0] and not any(up[1:]):
                        trail = trails.setdefault(idx, deque(maxlen=42))
                        trail.append(tip)
                        for j in range(1, len(trail)):
                            glow_line(frame, trail[j - 1], trail[j])
                        cv2.circle(frame, tip, 8, (190, 240, 255), -1, cv2.LINE_AA)
                        add_particles(tip, 1)
                        status = "SPELL TRAIL | INDEX FINGER"
                    else:
                        trails.pop(idx, None)
            else:
                trails.clear()

            update_particles(frame)
            cv2.rectangle(frame, (16, 16), (620, 92), (16, 13, 30), -1)
            cv2.rectangle(frame, (16, 16), (620, 92), (80, 145, 255), 1)
            cv2.putText(frame, "DOCTOR STRANGE | MAGIC INTERFACE V2",
                        (32, 47), cv2.FONT_HERSHEY_DUPLEX, .68,
                        (225, 238, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, status, (32, 75), cv2.FONT_HERSHEY_SIMPLEX,
                        .52, (100, 205, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, "Q: QUIT", (w - 125, h - 22),
                        cv2.FONT_HERSHEY_SIMPLEX, .55, (230, 230, 230), 1)
            cv2.imshow("Doctor Strange - Magic Hand Tracking V2", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
