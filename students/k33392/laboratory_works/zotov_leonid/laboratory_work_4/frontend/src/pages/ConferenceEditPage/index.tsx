import { useState, useEffect } from "react";
import axios from "axios";
import style from "./ConferenceEditPage.module.scss";
import { useNavigate, useParams } from "react-router-dom";
import { ConferenceData, TopicData } from "../MainPage";

export const ConferenceEditPage = () => {
  const { id } = useParams<{ id: string }>();
  const [title, setTitle] = useState<string>("");
  const [location, setLocation] = useState<string>("");
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [conditions, setConditions] = useState<string>("");
  const [topics, setTopics] = useState<TopicData[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<number[]>([]);
  const authToken = localStorage.getItem("authToken");
  const [conference, setConference] = useState<ConferenceData | null>(null);
  const nav = useNavigate();

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const headers = {
          Authorization: `Token ${authToken}`,
        };

        const response = await axios.get("http://127.0.0.1:8000/main/topics/", {
          headers,
        });
        setTopics(response.data);
      } catch (error) {
        console.error("Ошибка при загрузке тем:", error);
      }
    };

    fetchTopics();
  }, [authToken]);

  useEffect(() => {
    const fetchConferenceDetails = async () => {
      try {
        const headers = { Authorization: `Token ${authToken}` };
        const response = await axios.get(
          `http://127.0.0.1:8000/main/conferences/${id}/`,
          { headers }
        );
        if (response.status === 200) {
          const conference = response.data;
          setConference(conference);
          setTitle(conference.title);
          setLocation(conference.location);
          setStartDate(conference.start_date);
          setEndDate(conference.end_date);
          setDescription(conference.description);
          setConditions(conference.participation_conditions);
          setSelectedTopic(
            conference.topics.map((topic: TopicData) => topic.id)
          );
        }
      } catch (error) {
        console.error("Ошибка при получении информации о конференции:", error);
      }
    };

    fetchConferenceDetails();
  }, [id, authToken]);

  const handleTopicChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedId = parseInt(e.target.value, 10);
    setSelectedTopic([...selectedTopic, selectedId]);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const conferenceData = {
      title,
      location,
      start_date: startDate,
      end_date: endDate,
      description,
      participation_conditions: conditions,
      topics: selectedTopic,
    };

    try {
      const headers = { Authorization: `Token ${authToken}` };
      const response = await axios.put(
        `http://127.0.0.1:8000/main/conferences/${id}/`,
        conferenceData,
        { headers }
      );
      if (response.status === 200) {
        alert("Конференция успешно обновлена");
        nav(`/conference/${id}`);
      }
    } catch (error) {
      console.error("Ошибка при обновлении конференции:", error);
    }
  };

  if (!conference) {
    return <div>Загрузка...</div>;
  }

  return (
    <div className={style.editContainer}>
      <h1>Создание новой конференции</h1>
      <form onSubmit={handleSubmit} className={style.createForm}>
        <input
          className={style.createOrd}
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Название конференции"
          required
        />
        <select
          className={style.createOrd}
          onChange={handleTopicChange}
          required
        >
          <option value="">Выберите тему</option>
          {topics.map((topic) => (
            <option key={topic.id} value={topic.id}>
              {topic.name}
            </option>
          ))}
        </select>
        <input
          className={style.createOrd}
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Местоположение"
          required
        />
        <input
          className={style.createOrd}
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          placeholder="Дата начала"
          required
        />
        <input
          className={style.createOrd}
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          placeholder="Дата окончания"
          required
        />
        <textarea
          className={style.createArea}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Описание"
          required
        />
        <textarea
          className={style.createArea}
          value={conditions}
          onChange={(e) => setConditions(e.target.value)}
          placeholder="Условия участия"
          required
        />
        <button type="submit" className={style.submitBtn}>
          Отредактировать конференцию
        </button>
      </form>
    </div>
  );
};
