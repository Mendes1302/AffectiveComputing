CREATE TABLE song(song_id INTEGER PRIMARY KEY NOT NULL, 
                  song_name TEXT NOT NULL, 
                  lyrics TEXT NOT NULL, 
                  vagalume_song_url TEXT NOT NULL, 
                  vagalume_song_id TEXT NOT NULL)


CREATE TABLE artist(artist_id INTEGER PRIMARY KEY NOT NULL, 
                  song_id INTEGER NOT NULL, 
                  artist_full_name TEXT NOT NULL, 
                  vagalume_artist_id TEXT NOT NULL,
                  FOREIGN KEY(song_id) REFERENCES song(song_id))


CREATE TABLE emotion(emotion_id INTEGER PRIMARY KEY NOT NULL, 
                  name_emotion TEXT NOT NULL, 
                  synonym_emotion TEXT NOT NULL)


CREATE TABLE emotional_result (
    "emotinal_result_id" INTEGER PRIMARY KEY,
    "song_id" INTEGER,
    "model_name" TEXT,
    "admiração" FLOAT,
    "diversão" FLOAT,
    "raiva" FLOAT,
    "aborrecimento" FLOAT,
    "provação" FLOAT,
    "confusão" FLOAT,
    "curiosidade" FLOAT,
    "desejo" FLOAT,
    "decepção" FLOAT,
    "desaprovação" FLOAT,
    "nojo" FLOAT,
    "vergonha" FLOAT,
    "entusiasmo" FLOAT,
    "medo" FLOAT,
    "gratidão" FLOAT,
    "luto" FLOAT,
    "alegria" FLOAT,
    "amor" FLOAT,
    "nervosismo" FLOAT,
    "otimismo" FLOAT,
    "orgulho" FLOAT,
    "alívio" FLOAT,
    "remorso" FLOAT,
    "tristeza" FLOAT,
    "surpresa" FLOAT,
    "saudade" FLOAT,
    "inveja" FLOAT,
    "compaixão" FLOAT,
    "created_at" DATETIME,
    "updated_at" DATETIME,
    "deleted_at" DATETIME,
    FOREIGN KEY ("song_id") REFERENCES song("song_id"),
    PRIMARY KEY("emotinal_result_id" AUTOINCREMENT)
);


CREATE TABLE "inputs" (
	"inputs_id"	INTEGER NOT NULL UNIQUE,
	"text_name"	TEXT NOT NULL,
	"source"	TEXT NOT NULL,
	"emotion_id"	INTEGER NOT NULL,
	FOREIGN KEY("emotion_id") REFERENCES "emotion"("emotion_id"),
	PRIMARY KEY("inputs_id" AUTOINCREMENT)
)
