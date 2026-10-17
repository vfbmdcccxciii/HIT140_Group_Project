"""Shared paths and team-name mapping for HIT140 Assessment 3 (Darwin Group 27)."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
OUT = ROOT / "outputs"
for p in (RAW, PROC, OUT):
    p.mkdir(parents=True, exist_ok=True)
SEED = 140

# openfootball name -> (Transfermarkt name, Wikipedia name, eloratings.net name, confederation)
TEAMS = {
 'Algeria':('Algeria','Algeria','Algeria','CAF'), 'Argentina':('Argentina','Argentina','Argentina','CONMEBOL'),
 'Australia':('Australia','Australia','Australia','AFC'), 'Austria':('Austria','Austria','Austria','UEFA'),
 'Belgium':('Belgium','Belgium','Belgium','UEFA'),
 'Bosnia & Herzegovina':('Bosnia-Herzegovina','Bosnia and Herzegovina','Bosnia and Herzegovina','UEFA'),
 'Brazil':('Brazil','Brazil','Brazil','CONMEBOL'), 'Canada':('Canada','Canada','Canada','CONCACAF'),
 'Cape Verde':('Cape Verde','Cape Verde','Cape Verde','CAF'), 'Colombia':('Colombia','Colombia','Colombia','CONMEBOL'),
 'Croatia':('Croatia','Croatia','Croatia','UEFA'), 'Curaçao':('Curaçao','Curaçao','Curaçao','CONCACAF'),
 'Czech Republic':('Czechia','Czech Republic','Czechia','UEFA'), 'DR Congo':('Democratic Republic of the Congo','DR Congo','DR Congo','CAF'),
 'Ecuador':('Ecuador','Ecuador','Ecuador','CONMEBOL'), 'Egypt':('Egypt','Egypt','Egypt','CAF'),
 'England':('England','England','England','UEFA'), 'France':('France','France','France','UEFA'),
 'Germany':('Germany','Germany','Germany','UEFA'), 'Ghana':('Ghana','Ghana','Ghana','CAF'),
 'Haiti':('Haiti','Haiti','Haiti','CONCACAF'), 'Iran':('Iran','Iran','Iran','AFC'), 'Iraq':('Iraq','Iraq','Iraq','AFC'),
 'Ivory Coast':('Ivory Coast','Ivory Coast','Ivory Coast','CAF'), 'Japan':('Japan','Japan','Japan','AFC'),
 'Jordan':('Jordan','Jordan','Jordan','AFC'), 'Mexico':('Mexico','Mexico','Mexico','CONCACAF'),
 'Morocco':('Morocco','Morocco','Morocco','CAF'), 'Netherlands':('Netherlands','Netherlands','Netherlands','UEFA'),
 'New Zealand':('New Zealand','New Zealand','New Zealand','OFC'), 'Norway':('Norway','Norway','Norway','UEFA'),
 'Panama':('Panama','Panama','Panama','CONCACAF'), 'Paraguay':('Paraguay','Paraguay','Paraguay','CONMEBOL'),
 'Portugal':('Portugal','Portugal','Portugal','UEFA'), 'Qatar':('Qatar','Qatar','Qatar','AFC'),
 'Saudi Arabia':('Saudi Arabia','Saudi Arabia','Saudi Arabia','AFC'), 'Scotland':('Scotland','Scotland','Scotland','UEFA'),
 'Senegal':('Senegal','Senegal','Senegal','CAF'), 'South Africa':('South Africa','South Africa','South Africa','CAF'),
 'South Korea':('South Korea','South Korea','South Korea','AFC'), 'Spain':('Spain','Spain','Spain','UEFA'),
 'Sweden':('Sweden','Sweden','Sweden','UEFA'), 'Switzerland':('Switzerland','Switzerland','Switzerland','UEFA'),
 'Tunisia':('Tunisia','Tunisia','Tunisia','CAF'), 'Turkey':('Turkiye','Turkey','Turkey','UEFA'),
 'USA':('United States','United States','United States','CONCACAF'), 'Uruguay':('Uruguay','Uruguay','Uruguay','CONMEBOL'),
 'Uzbekistan':('Uzbekistan','Uzbekistan','Uzbekistan','AFC'),
}
HOSTS = {'USA', 'Mexico', 'Canada'}
