import { useState, useEffect } from "react";
import axios from "axios";
import style from "./ConferenceCreatePage.module.scss";
import { TopicData } from "../MainPage";

export const ConferenceCreatePage = () => {
  const [title, setTitle] = useState<string>("");
  const [location, setLocation] = useState<string>("");
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [conditions, setConditions] = useState<string>("");
  const [topics, setTopics] = useState<TopicData[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<number[]>([]);
  const authToken = localStorage.getItem("authToken");

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

  const handleTopicChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedId = parseInt(e.target.value, 10);
    setSelectedTopic([...selectedTopic, selectedId]);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const headers = {
      Authorization: `Token ${authToken}`,
    };

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
      const response = await axios.post(
        "http://127.0.0.1:8000/main/conferences/",
        conferenceData,
        { headers }
      );
      if (response.status === 201) {
        alert("Конференция успешно создана");
      }
    } catch (error) {
      console.error("Ошибка при создании конференции:", error);
    }
  };

  return (
    <div className={style.createContainer}>
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
          Создать конференцию
        </button>
      </form>
    </div>
  );
};
