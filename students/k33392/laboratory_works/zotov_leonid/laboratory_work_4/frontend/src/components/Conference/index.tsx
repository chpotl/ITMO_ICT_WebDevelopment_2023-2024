import style from "./Conference.module.scss";
import { TopicData } from "../../pages/MainPage";
import { Link } from "react-router-dom";
import axios from "axios";

type ConferenceProps = {
  id: number;
  author: string;
  title: string;
  topics: TopicData[];
  location: string;
  startDate: string;
  endDate: string;
  description: string;
  conditions: string;
};

export const Conference = ({
  id,
  author,
  title,
  topics,
  location,
  startDate,
  endDate,
  description,
  conditions,
}: ConferenceProps) => {
  const userId = localStorage.getItem("userId");
  const authToken = localStorage.getItem("authToken");

  const handleRegistration = async () => {
    try {
      const headers = {
        Authorization: `Token ${authToken}`,
      };

      const registrationData = {
        user: userId,
        conference: id,
        topic: topics[0].id,
      };

      const response = await axios.post(
        "http://127.0.0.1:8000/main/registrations/",
        registrationData,
        { headers }
      );

      if (response.status === 201) {
        alert("Регистрация на конференцию выполнена успешно!");
      }
    } catch (error) {
      console.error("Ошибка при регистрации на конференцию:", error);
      alert("Ошибка при регистрации!");
    }
  };
  return (
    <div className={style.confContainer}>
      <div className={style.mainWrapper}>
        <h3>{title}</h3>
        {topics.map((topic) => (
          <p>{topic.name}</p>
        ))}
      </div>
      <div className={style.infoWrapper}>
        <p>{author}</p>
        <p>{location}</p>
      </div>
      <p>
        {startDate} - {endDate}
      </p>
      <p>{description}</p>
      <div className={style.conditions}>
        <p>Условия для участия:</p>
        <p>{conditions}</p>
      </div>
      <div className={style.confButtons}>
        <Link to={`/conference/${id}`}>
          <button className={style.mainConfBtn}>Больше информации</button>
        </Link>
        <button className={style.mainConfBtn} onClick={handleRegistration}>
          Зарегистрироваться
        </button>
      </div>
    </div>
  );
};
