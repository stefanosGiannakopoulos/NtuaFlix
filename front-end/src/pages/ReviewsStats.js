import React, { useContext, useEffect, useState } from "react";
import AuthContext from "../context/AuthContext";
import NotRegistered from "./NotRegistered";
import "./ReviewsStats.css";
import axiosInstance from "../api/api";
import { Link } from "react-router-dom";
import Preloader from "../components/Preloader";
import { useLocation } from "react-router-dom";

export default function ReviewsStats() {
  const { pathname } = useLocation();

  const { authTokens } = useContext(AuthContext);

  const [Stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  function divide(x, y) {
    return (Math.round(10 * x / y)/10).toFixed(1);
  }

  function formatDate(date) {
    const options = { day: "2-digit", month: "long", year: "numeric" };
    const formattedDate = new Date(date).toLocaleDateString("gr-GR", options);

    // Split the formatted date into day, month, and year parts
    const [month, day, year] = formattedDate.split(" ");

    return `${day} ${month} ${year}`;
  }

  useEffect(() => {
    async function fetchStatistics() {
      try {
        const response = await axiosInstance.get(`/user_stats_reviews`, {
          headers: {
            "X-OBSERVATORY-AUTH": `${authTokens ? authTokens : "None"}`,
          },
        });

        if (response.status === 200) {
          setStats(response?.data);
          setIsLoading(false);
          console.log(response?.data);
        }
      } catch (err) {
        setIsLoading(false);
        console.log(err.message);
      }
    }

    fetchStatistics();
  }, [authTokens]);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  if (!authTokens) return <NotRegistered />;
  if (isLoading) return <Preloader />;

  return (
    <div className="page-container">
      {Stats &&
      Boolean(Stats.num_total_reviews) &&
      Boolean(Stats.user_num_reviews) ? (
        <>
          <div
            className="reviews_statistics-container"
            style={{ marginTop: 180, marginBottom: 270 }}
          >
            <div className="reviews_statistics-column">
              <div className="reviews_statistics-row">
                <h1 className="title-with-line" style={{ marginBottom: 10 }}>
                  General Statistics
                </h1>
                <ul>
                  <li>
                    <p style={{ marginTop: 20 }}>
                      In total, <b>{Stats.num_total_reviews}</b> reviews have
                      been posted by&nbsp;
                      <b>{Stats.num_total_users}</b> different users, meaning
                      that, on average,&nbsp; each user has posted{" "}
                      <b>
                        {divide(Stats.num_total_reviews, Stats.num_total_users)}
                      </b>
                      &nbsp; reviews. You have posted{" "}
                      <b>{Stats.user_num_reviews}</b> reviews.
                    </p>
                  </li>
                  <li>
                    <p style={{ marginTop: 20 }}>
                      The average user rating is <b>{Stats.average_stars}</b>
                      &nbsp; out of 5. Your average rating in your reviews is{" "}
                      <b>{Stats.user_avg_stars}</b> out of 5.
                    </p>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <h1 className="statistic-genres-title">
            Now, let's take a closer look at the reviews you have posted:
          </h1>

          <div className="reviews_statistics-container">
            <div className="reviews_statistics-column">
              <div className="reviews_statistics-row">
                <h1 className="title-with-line" style={{ marginBottom: 10 }}>
                  Your Highest Rated Titles
                </h1>
                <table>
                  <tr>
                    <th>Stars</th>
                    <th>Original Title</th>
                    <th>Date Posted</th>
                  </tr>
                  {Stats.highest_ranked_titles.map((titles) => {
                    const date = formatDate(titles.date_posted);
                    return (
                      <tr>
                        <td>{Stats.highest_ranking}/5</td>
                        <td>
                          <Link
                            className="a-transition"
                            to={`/movie/${titles.tconst}`}
                          >
                            {titles.original_title}
                          </Link>
                        </td>
                        <td>{date}</td>
                      </tr>
                    );
                  })}
                </table>
              </div>
            </div>
          </div>
          <div className="reviews_statistics-container">
            <div className="reviews_statistics-column">
              <div className="reviews_statistics-row">
                <h1 className="title-with-line" style={{ marginBottom: 10 }}>
                  Your Lowest Rated Titles
                </h1>
                <table>
                  <tr>
                    <th>Stars</th>
                    <th>Original Title</th>
                    <th>Date Posted</th>
                  </tr>
                  {Stats.lowest_ranked_titles.map((titles) => {
                    const date = formatDate(titles.date_posted);
                    return (
                      <tr>
                        <td>{Stats.lowest_ranking}/5</td>
                        <td>
                          <Link
                            className="a-transition"
                            to={`/movie/${titles.tconst}`}
                          >
                            {titles.original_title}
                          </Link>
                        </td>
                        <td>{date}</td>
                      </tr>
                    );
                  })}
                </table>
              </div>
            </div>
          </div>
          <div className="reviews_statistics-container">
            <div className="reviews_statistics-column">
              <div className="reviews_statistics-row">
                <h1 className="title-with-line" style={{ marginBottom: 10 }}>
                  Your Reviews With the Most Likes
                </h1>
                {Boolean(Stats.count_most_likes) ? (
                  <table>
                    <tr>
                      <th>Likes</th>
                      <th>Stars</th>
                      <th>Original Title</th>
                      <th>Date Posted</th>
                    </tr>
                    {Stats.most_liked.map((titles) => {
                      const date = formatDate(titles.date_posted);
                      return (
                        <tr>
                          <td>{Stats.count_most_likes}</td>
                          <td>{titles.stars}/5</td>
                          <td>
                            <Link
                              className="a-transition"
                              to={`/movie/${titles.tconst}`}
                            >
                              {titles.original_title}
                            </Link>
                          </td>
                          <td>{date}</td>
                        </tr>
                      );
                    })}
                  </table>
                ) : (
                  <p style={{ textAlign: "center", marginTop: 80 }}>
                    It looks like no one has liked any of your reviews :(
                  </p>
                )}
              </div>
            </div>
          </div>
          <div className="reviews_statistics-container">
            <div className="reviews_statistics-column">
              <div className="reviews_statistics-row">
                <h1 className="title-with-line" style={{ marginBottom: 10 }}>
                  Your Reviews With the Most Dislikes
                </h1>
                {Boolean(Stats.count_most_dislikes) ? (
                  <table>
                    <tr>
                      <th>Dislikes</th>
                      <th>Stars</th>
                      <th>Original Title</th>
                      <th>Date Posted</th>
                    </tr>
                    {Stats.most_disliked.map((titles) => {
                      const date = formatDate(titles.date_posted);
                      return (
                        <tr>
                          <td>{Stats.count_most_dislikes}</td>
                          <td>{titles.stars}/5</td>
                          <td>
                            <Link
                              className="a-transition"
                              to={`/movie/${titles.tconst}`}
                            >
                              {titles.original_title}
                            </Link>
                          </td>
                          <td>{date}</td>
                        </tr>
                      );
                    })}
                  </table>
                ) : (
                  <p style={{ textAlign: "center", marginTop: 80 }}>
                    It looks like no one has disliked any of your reviews :)
                  </p>
                )}
              </div>
            </div>
          </div>
        </>
      ) : (
        <div>
          <p style={{ textAlign: "center", marginTop: 250 }}>
            It looks like you haven't made any reviews yet!
          </p>
        </div>
      )}
    </div>
  );
}
