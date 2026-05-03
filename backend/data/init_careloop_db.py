import sqlite3
import datetime

def create_db():
    conn = sqlite3.connect('careloop.db')
    cursor = conn.cursor()

    # 1. patients
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        date_of_birth DATE,
        gender TEXT,
        address TEXT,
        risk_group TEXT DEFAULT 'Low' -- 'Low', 'Medium', 'High' (XGBoost prediction)
    )
    ''')

    # 2. chronic_conditions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chronic_conditions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        condition_name TEXT NOT NULL,
        diagnosed_date DATE,
        FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
    )
    ''')

    # 3. caregivers (Caregiver Loop)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS caregivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        full_name TEXT NOT NULL,
        relationship TEXT,
        phone TEXT,
        email TEXT,
        is_opt_in BOOLEAN DEFAULT 1,
        FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
    )
    ''')

    # 4. appointments (Adherence Loop)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_name TEXT,
        department TEXT,
        appointment_datetime DATETIME,
        status TEXT DEFAULT 'Scheduled', -- 'Scheduled', 'Confirmed', 'No-Show', 'Completed', 'Cancelled'
        no_show_risk_score REAL, -- XGBoost score
        recommended_time_slot TEXT, -- AI Suggested time
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
    )
    ''')

    # 5. medical_records (Post-Visit AI Bundle)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medical_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        patient_id INTEGER,
        diagnosis TEXT,
        doctor_notes TEXT,
        prescriptions TEXT,
        next_appointment_date DATE,
        ai_summary TEXT, -- Gemini Clinical Summary
        ai_video_url TEXT, -- Remotion + ElevenLabs personalized video
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(appointment_id) REFERENCES appointments(id),
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    ''')

    # 6. clinical_metrics (Clinical Progress Chart)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clinical_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        metric_name TEXT NOT NULL,
        metric_value REAL NOT NULL,
        unit TEXT,
        recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
    )
    ''')

    # 7. communication_logs (Tracking Adherence Loop actions)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS communication_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        appointment_id INTEGER,
        channel TEXT, -- 'SMS', 'App', 'Voice', 'Caregiver_Alert'
        message_level TEXT, -- 'Level_1', 'Level_2_Caregiver', 'Level_3_CSKH'
        content TEXT,
        sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT, -- 'Sent', 'Delivered', 'Failed'
        is_responded BOOLEAN DEFAULT 0,
        FOREIGN KEY(patient_id) REFERENCES patients(id),
        FOREIGN KEY(appointment_id) REFERENCES appointments(id)
    )
    ''')

    # Insert Sample Data
    
    # Clear existing data if any
    tables = ['communication_logs', 'clinical_metrics', 'medical_records', 'appointments', 'caregivers', 'chronic_conditions', 'patients']
    for table in tables:
        cursor.execute(f'DELETE FROM {table}')

    # Sample Patients
    patients = [
        (1, 'Nguyễn Văn An', '0901234567', 'an.nguyen@email.com', '1955-05-10', 'Nam', 'Quận 1, TP.HCM', 'High'),
        (2, 'Trần Thị Bình', '0912345678', 'binh.tran@email.com', '1960-08-15', 'Nữ', 'Quận 3, TP.HCM', 'Medium'),
        (3, 'Lê Văn Cường', '0923456789', 'cuong.le@email.com', '1950-12-20', 'Nam', 'Gò Vấp, TP.HCM', 'Low')
    ]
    cursor.executemany('INSERT INTO patients(id, full_name, phone, email, date_of_birth, gender, address, risk_group) VALUES(?,?,?,?,?,?,?,?)', patients)

    # Sample Chronic Conditions
    conditions = [
        (1, 1, 'Đái tháo đường type 2', '2015-05-01'),
        (2, 1, 'Tăng huyết áp', '2018-10-15'),
        (3, 2, 'Bệnh phổi tắc nghẽn mãn tính (COPD)', '2020-03-10'),
        (4, 3, 'Rối loạn lipid máu', '2021-07-22')
    ]
    cursor.executemany('INSERT INTO chronic_conditions(id, patient_id, condition_name, diagnosed_date) VALUES(?,?,?,?)', conditions)

    # Sample Caregivers
    caregivers = [
        (1, 1, 'Nguyễn Văn Tuấn', 'Con trai', '0987654321', 'tuan.nguyen@email.com', 1),
        (2, 2, 'Trần Văn Hoàng', 'Chồng', '0976543210', 'hoang.tran@email.com', 1)
    ]
    cursor.executemany('INSERT INTO caregivers(id, patient_id, full_name, relationship, phone, email, is_opt_in) VALUES(?,?,?,?,?,?,?)', caregivers)

    # Sample Appointments
    now = datetime.datetime.now()
    past_date = now - datetime.timedelta(days=30)
    future_date = now + datetime.timedelta(days=2)
    
    appointments = [
        (1, 1, 'BS. Phạm Văn Dũng', 'Nội tiết', past_date.strftime('%Y-%m-%d 08:30:00'), 'Completed', 0.85, 'Sáng giữa tuần'),
        (2, 1, 'BS. Phạm Văn Dũng', 'Nội tiết', future_date.strftime('%Y-%m-%d 09:00:00'), 'Scheduled', 0.88, 'Sáng thứ 3, 4'),
        (3, 2, 'BS. Lê Hữu Trí', 'Hô hấp', future_date.strftime('%Y-%m-%d 14:00:00'), 'Confirmed', 0.45, 'Chiều cuối tuần')
    ]
    cursor.executemany('INSERT INTO appointments(id, patient_id, doctor_name, department, appointment_datetime, status, no_show_risk_score, recommended_time_slot) VALUES(?,?,?,?,?,?,?,?)', appointments)

    # Sample Medical Records
    records = [
        (1, 1, 1, 'Đái tháo đường type 2 kiểm soát kém', 'Đường huyết lúc đói cao (8.5 mmol/L). Cần tăng liều Metformin.', 'Metformin 850mg x 2 lần/ngày. Diamicron 30mg x 1 lần/ngày.', (past_date + datetime.timedelta(days=30)).strftime('%Y-%m-%d'), 'Đường huyết của bác An đang hơi cao (8.5). Bác nhớ uống Metformin 2 lần sáng tối sau ăn, và Diamicron 1 lần buổi sáng. Hẹn bác 1 tháng sau tái khám nhé.', 'https://careloop.vn/video/patient/1/summary_1.mp4')
    ]
    cursor.executemany('INSERT INTO medical_records(id, appointment_id, patient_id, diagnosis, doctor_notes, prescriptions, next_appointment_date, ai_summary, ai_video_url) VALUES(?,?,?,?,?,?,?,?,?)', records)

    # Sample Clinical Metrics
    metrics = [
        (1, 1, 'Blood Glucose', 7.2, 'mmol/L', (past_date - datetime.timedelta(days=30)).strftime('%Y-%m-%d 08:00:00')),
        (2, 1, 'Blood Glucose', 8.5, 'mmol/L', past_date.strftime('%Y-%m-%d 08:00:00')),
        (3, 1, 'Systolic Blood Pressure', 140, 'mmHg', past_date.strftime('%Y-%m-%d 08:00:00'))
    ]
    cursor.executemany('INSERT INTO clinical_metrics(id, patient_id, metric_name, metric_value, unit, recorded_at) VALUES(?,?,?,?,?,?)', metrics)

    # Sample Communication Logs
    logs = [
        (1, 1, 2, 'App', 'Level_1', 'Bác An có lịch tái khám Nội tiết vào ngày mai. Vui lòng xác nhận.', now.strftime('%Y-%m-%d 08:00:00'), 'Delivered', 0),
        (2, 1, 2, 'Caregiver_Alert', 'Level_2_Caregiver', 'Bác An chưa xác nhận lịch tái khám ngày mai. Anh Tuấn nhắc bác giúp bệnh viện nhé.', now.strftime('%Y-%m-%d 10:00:00'), 'Sent', 0)
    ]
    cursor.executemany('INSERT INTO communication_logs(id, patient_id, appointment_id, channel, message_level, content, sent_at, status, is_responded) VALUES(?,?,?,?,?,?,?,?,?)', logs)

    conn.commit()
    conn.close()
    print("Database 'careloop.db' created and sample data inserted successfully!")

if __name__ == '__main__':
    create_db()
