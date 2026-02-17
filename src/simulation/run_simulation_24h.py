from core.simulation_engine import simulate_room_24h
from core.ingestion_engine import write_dataframe_to_influx

df = simulate_room_24h(samples=3000)

write_dataframe_to_influx(df, "room_sim_24h_v1")
