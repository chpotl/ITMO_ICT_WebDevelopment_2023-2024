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
