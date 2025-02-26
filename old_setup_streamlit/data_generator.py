import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Surgeon, Procedure, get_db

def populate_mock_data(db: Session, n_surgeons: int = 5, n_procedures: int = 100):
    """Populate database with mock surgical data."""
    # Create surgeons
    surgeons = []
    for i in range(n_surgeons):
        surgeon = Surgeon(name=f'Surgeon {i+1}')
        db.add(surgeon)
        surgeons.append(surgeon)
    db.commit()

    services = ['Melanoma', 'Gastrectomy', 'Whipple']

    for _ in range(n_procedures):
        service = np.random.choice(services)
        surgeon = np.random.choice(surgeons)

        # Generate realistic-looking data
        if service == 'Melanoma':
            los_mean, los_std = 3, 1
            complication_rate = 0.15
        elif service == 'Gastrectomy':
            los_mean, los_std = 7, 2
            complication_rate = 0.25
        else:  # Whipple
            los_mean, los_std = 10, 3
            complication_rate = 0.35

        procedure = Procedure(
            service=service,
            surgeon=surgeon,
            date=datetime.now() - timedelta(days=np.random.randint(0, 365)),
            length_of_stay=max(1, int(np.random.normal(los_mean, los_std))),
            complications=np.random.random() < complication_rate,
            t_stage=np.random.choice(['T1', 'T2', 'T3', 'T4']),
            p_stage=np.random.choice(['I', 'II', 'III', 'IV']),
            procedure_time=np.random.normal(180, 30)
        )
        db.add(procedure)

    db.commit()

def get_surgeon_metrics(db: Session, service: str, surgeon_name: str) -> dict:
    """Calculate metrics for a specific surgeon and service."""
    surgeon = db.query(Surgeon).filter(Surgeon.name == surgeon_name).first()
    procedures = db.query(Procedure).filter(
        Procedure.surgeon_id == surgeon.id,
        Procedure.service == service
    ).all()

    if not procedures:
        return {
            'total_procedures': 0,
            'avg_length_of_stay': 0,
            'complication_rate': 0
        }

    return {
        'total_procedures': len(procedures),
        'avg_length_of_stay': sum(p.length_of_stay for p in procedures) / len(procedures),
        'complication_rate': sum(1 for p in procedures if p.complications) / len(procedures) * 100
    }

def get_procedures_df(db: Session) -> pd.DataFrame:
    """Get all procedures as a pandas DataFrame."""
    procedures = db.query(Procedure).all()
    data = []
    for proc in procedures:
        data.append({
            'service': proc.service,
            'surgeon': proc.surgeon.name,
            'date': proc.date,
            'length_of_stay': proc.length_of_stay,
            'complications': proc.complications,
            't_stage': proc.t_stage,
            'p_stage': proc.p_stage,
            'procedure_time': proc.procedure_time
        })
    return pd.DataFrame(data)