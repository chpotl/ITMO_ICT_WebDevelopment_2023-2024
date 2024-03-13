# Лабораторная работа №4

## Общая инфрмация

Для реализации фронтенда был использован TypeScript, React, CSS-Modules (SASS). Для роутинга использовался React Router, для отправки запросов на бэкенд - axios.

## SignInPage.tsx

Функция для регистрации

```
const handleRegister = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/auth/users/", {
        email: email,
        username: userName,
        password: password,
      });

      if (response.status === 201) {
        const userId = response.data.id;
        localStorage.setItem("authToken", response.data.auth_token);
        localStorage.setItem("userId", userId);
        localStorage.setItem("username", userName);
        alert("Регистрация успешна");
        navigate("/main");
      }
    } catch (error) {
      console.error("Ошибка при регистрации:", error);
    }
  };
```

Функция для логина

```
const handleLogin = async () => {
    try {
      const loginResponse = await axios.post(
        "http://127.0.0.1:8000/auth/token/login/",
        {
          username: userName,
          password: password,
        }
      );

      if (loginResponse.status === 200) {
        localStorage.setItem("authToken", loginResponse.data.auth_token);
        const userResponse = await axios.get(
          "http://127.0.0.1:8000/auth/users/me/",
          {
            headers: {
              Authorization: `Token ${loginResponse.data.auth_token}`,
            },
          }
        );

        if (userResponse.status === 200) {
          const userId = userResponse.data.id;
          localStorage.setItem("userId", userId);
          localStorage.setItem("username", userName);
          alert("Вход выполнен успешно");
          navigate("/main");
        }
      }
    } catch (error) {
      console.error("Ошибка при входе:", error);
    }
  };
```

## MainPage.tsx

Функци для получения конференций пользователя и других пользователей с бэкенда

```
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
```

## ConferenceCreatePage.tsx

Функция для получения тем с бэкенда (для последующего его использования при создании конференции)

```
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
```

Функция для отправки формы создания конференции

```
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
```

## ConferencePage.tsx

Функция для получения деталей конференции и отзывов с бэкенда

```
  useEffect(() => {
    const fetchConferenceDetails = async () => {
      try {
        const headers = {
          Authorization: `Token ${authToken}`,
        };
        const response = await axios.get(
          `http://127.0.0.1:8000/main/conferences/${id}/`,
          { headers }
        );

        if (response.status === 200) {
          setConference(response.data);
        }
      } catch (error) {
        console.error("Ошибка при получении информации о конференции:", error);
      }
    };

    const fetchReviews = async () => {
      try {
        const headers = {
          Authorization: `Token ${authToken}`,
        };
        const response = await axios.get(
          `http://127.0.0.1:8000/main/reviews/`,
          { headers }
        );

        if (response.status === 200) {
          const filteredReviews = response.data.filter(
            (review: Review) => review.conference.id === Number(id)
          );
          setReviews(filteredReviews);
        }
      } catch (error) {
        console.error("Ошибка при получении отзывов:", error);
      }
    };

    fetchConferenceDetails();
    fetchReviews();
  }, [id, authToken]);
```

Функция для отправки формы написания отзыва

```
  const handleReviewSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();
    try {
      const headers = {
        Authorization: `Token ${authToken}`,
      };

      const currentDate = new Date().toISOString().split("T")[0];

      const reviewData = {
        text: reviewText,
        comment_text: commentText,
        rating: reviewRating,
        conference: Number(id),
        comment_date: currentDate,
        user: userId,
      };
      const response = await axios.post(
        `http://127.0.0.1:8000/main/reviews/`,
        reviewData,
        { headers }
      );
      if (response.status === 201) {
        setReviews([...reviews, response.data]);
        setReviewText("");
        setCommentText("");
        setReviewRating(1);
      }
    } catch (error) {
      console.error("Ошибка при отправке отзыва:", error);
    }
  };
```

## Conference.tsx

Функция для регистрации пользователя на конференцию

```
import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";
import style from "./ConferencePage.module.scss";
import { ConferenceData } from "../MainPage";
import { Link } from "react-router-dom";

type Review = {
  id: number;
  text: string;
  comment_text: string;
  rating: number;
  conference: { id: number; author: string; title: string };
  user: number;
  comment_date: string;
};

export const ConferencePage = () => {
  const { id } = useParams<{ id: string }>();
  const [conference, setConference] = useState<ConferenceData | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [reviewText, setReviewText] = useState("");
  const [commentText, setCommentText] = useState("");
  const [reviewRating, setReviewRating] = useState(1);
  const authToken = localStorage.getItem("authToken");
  const userId = localStorage.getItem("userId");
  const username = localStorage.getItem("username");
  const nav = useNavigate();

  useEffect(() => {
    const fetchConferenceDetails = async () => {
      try {
        const headers = {
          Authorization: `Token ${authToken}`,
        };
        const response = await axios.get(
          `http://127.0.0.1:8000/main/conferences/${id}/`,
          { headers }
        );

        if (response.status === 200) {
          setConference(response.data);
        }
      } catch (error) {
        console.error("Ошибка при получении информации о конференции:", error);
      }
    };

    const fetchReviews = async () => {
      try {
        const headers = {
          Authorization: `Token ${authToken}`,
        };
        const response = await axios.get(
          `http://127.0.0.1:8000/main/reviews/`,
          { headers }
        );

        if (response.status === 200) {
          const filteredReviews = response.data.filter(
            (review: Review) => review.conference.id === Number(id)
          );
          setReviews(filteredReviews);
        }
      } catch (error) {
        console.error("Ошибка при получении отзывов:", error);
      }
    };

    fetchConferenceDetails();
    fetchReviews();
  }, [id, authToken]);

  const handleReviewSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();
    try {
      const headers = {
        Authorization: `Token ${authToken}`,
      };

      const currentDate = new Date().toISOString().split("T")[0];

      const reviewData = {
        text: reviewText,
        comment_text: commentText,
        rating: reviewRating,
        conference: Number(id),
        comment_date: currentDate,
        user: userId,
      };
      const response = await axios.post(
        `http://127.0.0.1:8000/main/reviews/`,
        reviewData,
        { headers }
      );
      if (response.status === 201) {
        setReviews([...reviews, response.data]);
        setReviewText("");
        setCommentText("");
        setReviewRating(1);
      }
    } catch (error) {
      console.error("Ошибка при отправке отзыва:", error);
    }
  };

  if (!conference) {
    return <div>Конференция не найдена</div>;
  }

  const handleDelete = async () => {
    if (window.confirm("Вы уверены, что хотите удалить эту конференцию?")) {
      try {
        const headers = {
          Authorization: `Token ${authToken}`,
        };
        const response = await axios.delete(
          `http://127.0.0.1:8000/main/conferences/${id}/`,
          { headers }
        );

        if (response.status === 204) {
          alert("Конференция успешно удалена");
          nav("/main");
        }
      } catch (error) {
        console.error("Ошибка при удалении конференции:", error);
        alert("Не удалось удалить конференцию");
      }
    }
  };

  return (
    <div className={style.confPageContainer}>
      <div className={style.confInfo}>
        <h1>{conference.title}</h1>
        <p>Автор: {conference.author}</p>
        {conference.topics.map((topic) => (
          <p>Тема: {topic.name}</p>
        ))}
        <p>Описание: {conference.description}</p>
        <p>Место проведения: {conference.location}</p>
        <p>Дата начала: {conference.start_date}</p>
        <p>Дата окончания: {conference.end_date}</p>
        <p>Условия участия: {conference.participation_conditions}</p>
      </div>
      <>
        {username == conference.author ? (
          <>
            <Link to={`/conference_edit/${id}`}>
              <button className={style.submitBtn}>Редактировать</button>
            </Link>
            <button className={style.deleteBtn} onClick={handleDelete}>
              Удалить
            </button>
          </>
        ) : (
          <></>
        )}
      </>
      <div className={style.confPageReviews}>
        <h2>Отзывы:</h2>
        {reviews.map((review) => (
          <div key={review.id} className={style.confReview}>
            <p>Текст отзыва: {review.text}</p>
            <p>Комментарий: {review.comment_text}</p>
            <p>Рейтинг: {review.rating}</p>
            <p>Дата комментария: {review.comment_date}</p>
          </div>
        ))}
        <form onSubmit={handleReviewSubmit} className={style.confReviewForm}>
          <h2>Оставьте отзыв</h2>
          <textarea
            className={style.confArea}
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            placeholder="Текст отзыва"
            required
          />
          <textarea
            className={style.confArea}
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            placeholder="Комментарий к отзыву"
          />
          <select
            className={style.confOrd}
            value={reviewRating}
            onChange={(e) => setReviewRating(Number(e.target.value))}
            required
          >
            {[...Array(10).keys()].map((number) => (
              <option key={number + 1} value={number + 1}>
                {number + 1}
              </option>
            ))}
          </select>
          <button className={style.submitBtn} type="submit">
            Оставить отзыв
          </button>
        </form>
      </div>
    </div>
  );
};
```

##ConferenceEditPage.tsx

```
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
```
