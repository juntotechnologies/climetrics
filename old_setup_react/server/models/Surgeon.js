const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Surgeon = sequelize.define('Surgeon', {
  name: {
    type: DataTypes.STRING,
    unique: true,
    allowNull: false
  }
});

module.exports = Surgeon; 