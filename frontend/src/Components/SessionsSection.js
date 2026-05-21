import React from "react";

function SessionsSection({ sessions }) {

  return (

    <div className="session-table">

      <h2>Sessions</h2>

      <table>

        <thead>

          <tr>

            <th>Session ID</th>
            <th>Batch</th>
            <th>Status</th>
            <th>Allocated</th>

          </tr>

        </thead>

        <tbody>

          {
            sessions.map((session) => (

              <tr key={session.session_id}>

                <td>{session.session_id}</td>

                <td>{session.batch_id}</td>

                <td>{session.session_status}</td>

                <td>{session.session_allocated}</td>

              </tr>

            ))
          }

        </tbody>

      </table>

    </div>
  );
}

export default SessionsSection;