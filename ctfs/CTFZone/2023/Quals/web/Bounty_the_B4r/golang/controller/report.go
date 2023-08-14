package controller

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/google/uuid"
	"github.com/val1d/bb_ctf/api"
	"github.com/val1d/bb_ctf/db"
)

const PRIV_MIN = 100000

func bindAndValidateSubmitReportRequest(r *http.Request) (api.SubmitReportRequest, error) {
	var req api.SubmitReportRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		return req, err
	}

	if req.Program == nil || req.Description == nil || req.Severity == nil || req.Weakness == nil || req.Title == nil {
		return req, fmt.Errorf("missed json field")
	}

	if *req.Program == "" || *req.Description == "" || *req.Severity == "" || *req.Weakness == "" || *req.Title == "" {
		return req, fmt.Errorf("empty fields")
	}

	return req, nil
}

func (s *server) PostReport(w http.ResponseWriter, r *http.Request) {
	req, err := bindAndValidateSubmitReportRequest(r)
	if err != nil {
		api.HandleError(err, w)
		return
	}

	pUuid := *req.Program
	var bbProgram db.BBProgram
	res := s.db.Impl.First(&bbProgram, "id = ?", pUuid)

	if res.Error != nil || res.RowsAffected != 1 {
		api.HandleError(fmt.Errorf("wrong program Id"), w)
		return
	}

	userID := getUserID(r)
	var progMembers db.ProgramMembers
	res = s.db.Impl.First(&progMembers, "user_id = ? AND program_id = ?", userID, bbProgram.ID)
	if res.Error != nil || res.RowsAffected != 1 {
		api.HandleError(fmt.Errorf("you're not a member of this program"), w)
		return
	}

	report, err := s.db.CreateReport(
		*req.Title,
		*req.Description,
		bbProgram.ID,
		*req.Severity,
		*req.Weakness,
		userID,
	)

	if err != nil {
		api.HandleError(fmt.Errorf("error occured"), w)
		return
	}

	resp := api.SubmitReportResponse{ReportID: &report.UUID}
	api.EncodeResponse(w, resp)
}

func (s *server) GetReportRUuid(w http.ResponseWriter, r *http.Request, rUuid uuid.UUID, params api.GetReportRUuidParams) {
	userID := getUserID(r)
	var user db.Users
	s.db.Impl.Find(&user, "id = ?", userID)

	if user.Pow != params.Pow {
		api.HandleError(fmt.Errorf("wrong proof of work"), w)
		return
	}

	user.Pow = getRandomString(9)
	s.db.Impl.Save(&user)

	strUuid := rUuid.String()
	var report db.Report
	result := s.db.Impl.First(&report, "uuid = ?", strUuid)

	if result.Error != nil {
		api.HandleError(fmt.Errorf("wrong report id"), w)
		return
	}
	var bbProgram db.BBProgram
	s.db.Impl.First(&bbProgram, "id = ?", report.Program)

	if bbProgram.Type == ProgramTypePrivate {
		var progMembers db.ProgramMembers
		result = s.db.Impl.First(&progMembers, "user_id = ? AND program_id = ?", userID, bbProgram.ID)
		if result.Error != nil || result.RowsAffected != 1 {
			api.HandleError(fmt.Errorf("you're not a member of this program"), w)
			return
		}
	}

	resp := api.GetReportResponse{Title: &report.Title, Description: &report.Description, Severity: &report.Severity, Weakness: &report.Weakness, Published: &report.Published, ProgramId: &bbProgram.ID, ProgramName: &bbProgram.Name}
	api.EncodeResponse(w, resp)
}

func (s *server) GetDiscovery(w http.ResponseWriter, r *http.Request) {
	bznCtfBbProgName := "CTFZone Private Program"
	var bbProgram db.BBProgram
	s.db.Impl.First(&bbProgram, "name = ?", bznCtfBbProgName)

	var hotTopicReport db.Report
	res := s.db.Impl.First(&hotTopicReport, "id = 1 AND program = ?", bbProgram.ID)
	if res.Error != nil || res.RowsAffected == 0 {
		api.HandleError(fmt.Errorf("No hot topics :("), w)
		return
	}

	resp := api.GetDiscoveryResponse{Title: &hotTopicReport.Title, Severity: &hotTopicReport.Severity, Published: &hotTopicReport.Published}
	api.EncodeResponse(w, &resp)
}
