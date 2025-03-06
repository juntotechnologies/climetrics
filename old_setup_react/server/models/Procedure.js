const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Procedure = sequelize.define('Procedure', {
  service: {
    type: DataTypes.STRING,
    allowNull: false
  },
  date: {
    type: DataTypes.DATE,
    allowNull: false
  },
  lengthOfStay: {
    type: DataTypes.INTEGER
  },
  complications: {
    type: DataTypes.BOOLEAN,
    defaultValue: false
  },
  tStage: DataTypes.STRING,
  pStage: DataTypes.STRING,
  procedureTime: DataTypes.FLOAT
});

module.exports = Procedure; 