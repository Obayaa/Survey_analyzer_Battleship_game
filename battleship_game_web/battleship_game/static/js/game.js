let isPlayerTurn = true;
const statusDisplay = document.getElementById('game-status');
let boardData = Array(10).fill().map(() => Array(10).fill('')); // Initialize with grid size


function createBoard(boardId, boardData, isPlayer) {
    const board = document.getElementById(boardId);
    board.style.gridTemplateColumns = `repeat(${boardData.length}, 1fr)`;
    board.innerHTML = '';  // Clear the board for fresh rendering

    boardData.forEach((row, rowIndex) => {
        row.forEach((cell, colIndex) => {
            const div = document.createElement('div');
            div.classList.add('cell');
            
            // Show ships on the player's board only
            if (isPlayer && cell === 'S') {
                console.log(`Adding ship class to cell at row ${rowIndex}, col ${colIndex}`);
                div.classList.add('ship');
            }
            // Add hit/miss classes if cell has been targeted
            if (cell === 'H') {
                div.classList.add('hit');
                div.textContent = 'X';
            } else if (cell === 'M') {
                div.classList.add('miss');
                div.textContent = 'O';
            }
            
            // Attach event listeners only to the computer's board if it's the player's turn
            if (!isPlayer) {
                div.addEventListener('click', () => handleCellClick(rowIndex, colIndex));
            }

            board.appendChild(div);
        });
    });
}

function handleCellClick(row, col) {
    // Check if it's player's turn and the cell hasn't been clicked before
    const board = document.getElementById('computer-board');
    const cellIndex = row * boardData.length + col;
    const cell = board.children[cellIndex];
    
    if (!isPlayerTurn || cell.classList.contains('hit') || cell.classList.contains('miss')) {
        return;
    }
    
    makeMove(row, col);
}

function makeMove(row, col) {
    if (!isPlayerTurn) return;
    
    isPlayerTurn = false;
    updateStatus("Processing your move...");
    
    fetch('/make_move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row, col })
    })
    .then(response => response.json())
    .then(data => {
        // Handle player's move
        const playerResult = data.player;
        updateCell('computer-board', row, col, playerResult.result);
        updateStatus(playerResult.message);

        if (playerResult.game_over) {
            handleGameOver(playerResult.winner);
            return;
        }

        // Handle computer's move with delay
        setTimeout(() => {
            updateStatus("Computer is thinking...");
            fetch('/computer_turn', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(computerData => {
                updateCell('player-board', computerData.row, computerData.col, computerData.result);
                updateStatus(computerData.message);

                if (computerData.game_over) {
                    handleGameOver(computerData.winner);
                } else {
                    isPlayerTurn = true;
                    updateStatus("Your turn!");
                }
            })
            .catch(error => {
                console.error('Error during computer turn:', error);
                isPlayerTurn = true;
                updateStatus("Error occurred. Your turn!");
            });
        }, 1000);
    })
    .catch(error => {
        console.error('Error during player move:', error);
        isPlayerTurn = true;
        updateStatus("Error occurred. Please try again!");
    });
}

function updateCell(boardId, row, col, result) {
    const board = document.getElementById(boardId);
    const cellIndex = row * boardData.length + col;
    const cell = board.children[cellIndex];
    
    if (result === 'hit') {
        cell.classList.add('hit');
        cell.textContent = 'X';
    } else if (result === 'miss') {
        cell.classList.add('miss');
        cell.textContent = 'O';
    }
}

function updateStatus(message) {
    if (statusDisplay) {
        statusDisplay.textContent = message;
    }
}

function handleGameOver(winner) {
    const modal = document.getElementById('game-over-modal');
    const winnerText = document.getElementById('winner-text');
    if (winnerText) {
        winnerText.textContent = `${winner} wins!`;
    }
    if (modal) {
        modal.style.display = 'block';
    }
}

function restartGame() {
    // Reset grid data for both player and computer boards
    boardData = Array(10).fill().map(() => Array(10).fill(''));
    playerBoard = Array(10).fill().map(() => Array(10).fill(''));

    // Clear and recreate the grids on the UI
    createBoard('player-board', playerBoard, true);
    createBoard('computer-board', boardData, false);

    // Hide the game-over modal
    const modal = document.getElementById('game-over-modal');
    if (modal) modal.style.display = 'none';

    // Reset player turn and status display
    isPlayerTurn = true;
    updateStatus("Your turn!");

    // Optionally send a request to initialize server-side data, if necessary
    fetch('/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `grid_size=${boardData.length}`
    }).catch(error => {
        console.error('Error restarting game on server:', error);
    });
}


// Initialize boards when the page loads
window.onload = function() {
    // Get the grid size from the form input if it exists
    const gridSizeInput = document.getElementById('grid_size');
    if (gridSizeInput) {
        const gridSize = parseInt(gridSizeInput.value);
        boardData = Array(gridSize).fill().map(() => Array(gridSize).fill(''));
        playerBoard = Array(gridSize).fill().map(() => Array(gridSize).fill(''));
    }
    
    createBoard('player-board', playerBoard, true);
    createBoard('computer-board', boardData, false);
};