QUnit.test("contructorRoom", function(assert) {
    boards = [];
    room = new Room(-5, "TestRoom", 400, "room for testing", [1, 2, 3], [1, 2, 3], boards);
    assert.equal(room.toString(), "TestRoom");
    assert.notEqual(room.toString(), "TestRoomBlabla");
    assert.equal(room.boards, boards);
    //assert.equal(room.hasProjector(), false);
})