import style from "./MainPage.module.scss";
import axios from "axios";
import { useState, useEffect } from "react";
import { Conference } from "../../components/Conference";
import { Link } from "react-router-dom";

export type TopicData = {
  id: number;
  name: string;
};

export type ConferenceData = {
  id: number;
  author: string;
  title: string;
  topics: TopicData[];
  location: string;
  start_date: string;
  end_date: string;
  description: string;
  participation_conditions: string;
};

export const MainPage = () => {
  const [conferences, setConferences] = useState<ConferenceData[]>([]);
  const [myConferences, setMyConferences] = useState<ConferenceData[]>([]);
  const username = localStorage.getItem("username");
  const authToken = localStorage.getItem("authToken");

  useEffect(() => {
    const fetchConferences = async () => {
      try {
        if (!authToken) {
          console.error("Токен отсутствует в localStorage");
          return;
        }
        const headers = {
          Authorization: `Token ${authToken}`,
        };

        const response = await axios.get(
          "http://127.0.0.1:8000/main/conferences/",
          { headers }
        );

        if (response.status === 200) {
          const myConfs = response.data.filter(
            (conference: ConferenceData) => conference.author === username
          );
          const otherConfs = response.data.filter(
            (conference: ConferenceData) => conference.author !== username
          );

          setMyConferences(myConfs);
          setConferences(otherConfs);
        }
      } catch (error) {
        console.error("Ошибка при получении списка конференций:", error);
      }
    };

    fetchConferences();
  }, [authToken, username]);

  return (
    <div className={style.mainContainer}>
      <h1>Добро пожаловать, {username}!</h1>
      <div className={style.myConf}>
        <h2>Мои конференции:</h2>
        <Link to="/conference_create">
          <button className={style.createConfBtn}>Создать конференцию</button>
        </Link>
        {myConferences.map((conference: ConferenceData) => {
          const props = {
            id: conference.id,
            author: conference.author,
            title: conference.title,
            topics: conference.topics,
            location: conference.location,
            startDate: conference.start_date,
            endDate: conference.end_date,
            description: conference.description,
            conditions: conference.participation_conditions,
          };
          return <Conference {...props} />;
        })}
      </div>
      <div className={style.confSelection}>
        <h2>Список конференций:</h2>
        {conferences.map((conference: ConferenceData) => {
          const props = {
            id: conference.id,
            author: conference.author,
            title: conference.title,
            topics: conference.topics,
            location: conference.location,
            startDate: conference.start_date,
            endDate: conference.end_date,
            description: conference.description,
            conditions: conference.participation_conditions,
          };
          console.log(conference);
          return <Conference {...props} />;
        })}
      </div>
    </div>
  );
};
