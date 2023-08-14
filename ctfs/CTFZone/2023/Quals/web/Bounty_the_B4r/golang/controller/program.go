package controller

import (
	"fmt"
	"net/http"

	"github.com/google/uuid"
	"github.com/val1d/bb_ctf/api"
	"github.com/val1d/bb_ctf/db"
)

const (
	ProgramTypePublic = iota
	ProgramTypePrivate
)

func (s *server) GetPrograms(w http.ResponseWriter, r *http.Request) {
	var programs []db.BBProgram
	res := s.db.Impl.Find(&programs)
	if res.Error != nil {
		api.HandleError(fmt.Errorf("error occured"), w)
		return
	}

	resp := make([]api.Program, 0)
	for _, item := range programs {
		id := item.ID
		name := item.Name
		pt := int(item.Type)
		resp = append(resp, api.Program{Id: &id, Name: &name, ProgramType: &pt})
	}

	api.EncodeResponse(w, &resp)
}

func (s *server) PostProgramPUuidJoin(w http.ResponseWriter, r *http.Request, pUuid uuid.UUID) {
	userID := getUserID(r)
	var user db.Users
	s.db.Impl.Find(&user, "id = ?", userID)

	strUuid := pUuid.String()
	var bbProgram db.BBProgram
	res := s.db.Impl.First(&bbProgram, "id = ?", strUuid)
	if res.Error != nil || res.RowsAffected != 1 {
		api.HandleError(fmt.Errorf("wrong program Id"), w)
		return
	}

	if bbProgram.Type == ProgramTypePrivate && user.Reputation < PRIV_MIN {
		api.HandleError(fmt.Errorf("low reputation, try harder"), w)
		return
	}

	var progMembers db.ProgramMembers
	res = s.db.Impl.First(&progMembers, "user_id = ? AND program_id = ?", user.ID, bbProgram.ID)

	if res.RowsAffected >= 1 {
		api.HandleError(fmt.Errorf("you're already member of this program"), w)
		return
	}

	membership := db.ProgramMembers{
		ProgramID: bbProgram.ID,
		UserID:    user.ID,
	}

	res = s.db.Impl.Create(&membership)
	if res.Error != nil || res.RowsAffected != 1 {
		api.HandleError(fmt.Errorf("error occured"), w)
		return
	}

	respText := "Successfully joined."
	resp := api.JoinProgramResponse{Success: &respText}
	api.EncodeResponse(w, &resp)
}

func (s *server) GetProgramJoined(w http.ResponseWriter, r *http.Request) {
	userID := getUserID(r)
	var progMembers []db.ProgramMembers
	res := s.db.Impl.Find(&progMembers, "user_id = ?", userID)
	if res.Error != nil {
		api.HandleError(fmt.Errorf("error occured"), w)
		return
	}

	usersPrograms := []string{}
	for _, member := range progMembers {
		usersPrograms = append(usersPrograms, member.ProgramID)
	}

	resp := api.GetProgramJoinedResponse{Programs: &usersPrograms}
	api.EncodeResponse(w, &resp)
}
