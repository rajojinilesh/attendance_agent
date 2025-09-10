from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Dummy data: [classes_attended, classes_missed]
X = np.array([[10, 2], [9, 3], [6, 6], [3, 9]])
y = np.array([1, 1, 0, 0])  # 1 = likely present, 0 = likely absent

model = RandomForestClassifier()
model.fit(X, y)

def predict_attendance(attended, missed):
    return model.predict([[attended, missed]])[0]

print(predict_attendance(7, 3))
