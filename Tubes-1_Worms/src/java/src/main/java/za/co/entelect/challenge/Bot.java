package za.co.entelect.challenge;

import za.co.entelect.challenge.command.*;
import za.co.entelect.challenge.entities.*;
import za.co.entelect.challenge.enums.CellType;
import za.co.entelect.challenge.enums.Direction;
import za.co.entelect.challenge.enums.PowerUpType;

import java.util.*;
import java.util.stream.Collectors;

public class Bot {

    private Random random;
    private GameState gameState;
    private Opponent opponent;
    private MyWorm currentWorm;
    private MyWorm[] otherWorm;

    //Inisialisasi objek Bot
    public Bot(Random random, GameState gameState) {
        this.random = random;
        this.gameState = gameState;
        this.opponent = gameState.opponents[0];
        this.currentWorm = getCurrentWorm(gameState);
        this.otherWorm = getOtherWorm(gameState);
    }

    // Method untuk mendapatkan cacing yang aktif pada suatu round, digunakan untuk inisialisasi cacing
    private MyWorm getCurrentWorm(GameState gameState) {
        return Arrays.stream(gameState.myPlayer.worms)
                .filter(myWorm -> myWorm.id == gameState.currentWormId)
                .findFirst()
                .get();
    }

    // Method untuk mendapatkan cacing lainnya yang tidak sedang aktif dalam round tersebut
    private MyWorm[] getOtherWorm(GameState gameState) {
        MyWorm[] otherWorm;
        otherWorm = new MyWorm[2];
        int i = 0;
        for (MyWorm oWorm : gameState.myPlayer.worms){
            if (oWorm.id != gameState.currentWormId){
                otherWorm[i] = oWorm;
                i++;
            }
        }
        return otherWorm;
    }

    // Method untuk mendapatkan cacing musuh terdekat
    // Salah satu pengimplementasian strategi greedy dimana menargetkan cacing musuh dengan jarak yang terdekat
    private Worm getClosestEnemyWorm(){
        int minVal = euclideanDistance(opponent.worms[0].position.x, opponent.worms[0].position.y, currentWorm.position.x, currentWorm.position.y);
        Worm tempWorm = opponent.worms[0];
        for (Worm oWorm : opponent.worms){
            if(oWorm.health>0){
                int distance = euclideanDistance(oWorm.position.x, oWorm.position.y, currentWorm.position.x, currentWorm.position.y);
                if (minVal > distance){
                    minVal = distance;
                    tempWorm = oWorm;
                }
            }
        }
        return tempWorm;
    }

    // Method untuk mendapatkan cacing dengan darah paling sedikit
    // Salah satu pengimplementasian strategi greedy dimana menargetkan cacing musuh dengan jarak terdekat
    private Worm getLeastHPEnemy(){
        Worm tempWorm = opponent.worms[0];
        int minHP = 9999;
        for (Worm oWorm : opponent.worms){
            if(oWorm!=null) {
                int minHP2 = oWorm.health;
                if (minHP > minHP2 && minHP2 > 0) {
                    minHP = minHP2;
                    tempWorm = oWorm;
                }
            }
        }
        return tempWorm;
    }

    // Method untuk menentukan apakah musuh berada dalam jangkauan shoot
    private boolean isOpponentInShootRange(MyWorm cacingku, Worm musuh){
        Set<String> cells = constructFireDirectionLines(cacingku.weapon.range)
                .stream()
                .flatMap(Collection::stream)
                .map(cell -> String.format("%d_%d", cell.x, cell.y))
                .collect(Collectors.toSet());

        String enemyPosition = String.format("%d_%d", musuh.position.x, musuh.position.y);
        if (cells.contains(enemyPosition)) {
            return true;
        }

        return false;
    }

    // Method untuk menentukan apakah musuh dalam jangkauan banana bomb
    private boolean isOpponentInBananaRange(MyWorm cacingku, Worm musuh){
        int range = euclideanDistance(musuh.position.x, musuh.position.y, cacingku.position.x, cacingku.position.y);
        if (cacingku.id == 2) {
            if (range<=cacingku.bananaBombs.range && range > cacingku.bananaBombs.damageRadius && cacingku.bananaBombs.count > 0)
            return true;
        }

        return false;
    }

    // Method untuk menentukan apakah musuh dalam jangkauan snowball
    private boolean isOpponentInSnowballRange(MyWorm cacingku, Worm musuh){
        int range = euclideanDistance(musuh.position.x, musuh.position.y, cacingku.position.x, cacingku.position.y);
        if (cacingku.id == 3) {
            if (range<=cacingku.snowBalls.range && range > cacingku.snowBalls.freezeRadius && cacingku.snowBalls.count > 0)
                return true;
        }

        return false;
    }

    // Method untuk menentukan apakah ada cacing teman yang sedang dalam bahaya
    private boolean isOtherWormInDanger(){
        for (MyWorm friendWorm : otherWorm){
            if(friendWorm!=null) {
                Worm enemyWorm = getFirstWormInRange(friendWorm);
                boolean danger = false;
                for (Worm enemy : opponent.worms) {
                    if(enemy!=null) {
                        int radius = euclideanDistance(friendWorm.position.x, friendWorm.position.y, enemy.position.x, enemy.position.y);
                        if (radius <= 5) {
                            danger = true;
                            break;
                        }
                    }
                }
                if (enemyWorm != null || danger) {
                    return true;
                }
            }
        }
        return false;
    }

    // Method untuk mendapatkan cacing teman yang dalam bahaya
    private MyWorm getFriendInDanger(){
        for (MyWorm friendWorm : otherWorm){
            if(friendWorm!=null) {
                Worm enemyWorm = getFirstWormInRange(friendWorm);
                boolean danger = false;
                if (enemyWorm == null) {
                    for (Worm enemy : opponent.worms) {
                        if (enemy != null) {
                            if (isOpponentInSnowballRange(friendWorm, enemy) || isOpponentInBananaRange(friendWorm, enemy)) {
                                danger = true;
                                break;
                            }
                        }
                    }
                }

                if (enemyWorm != null || danger) {
                    return friendWorm;
                }

            }
        }
        return null;
    }

    // Method untuk mendapatkan musuh yang menyerang cacing teman
    private Worm getEnemyFriendInDanger(){
        for (MyWorm friendWorm : otherWorm){
            if(friendWorm!=null) {
                Worm enemyWorm = getFirstWormInRange(friendWorm);
                boolean danger = false;
                if (enemyWorm == null) {
                    for (Worm enemy : opponent.worms) {
                        if(enemy!=null) {
                            if(enemy.health>0) {
                                if (isOpponentInSnowballRange(friendWorm, enemy) || isOpponentInBananaRange(friendWorm, enemy)) {
                                    return enemy;
                                }
                            }
                        }
                    }
                }

                if (enemyWorm != null) {
                    return enemyWorm;
                }
            }
        }
        return null;
    }

    // Method untuk mendapatkan cacing yang menyerang currentWorm
    private Worm getCurrWormInDanger(){
        for (Worm enemy : opponent.worms){
            if(enemy != null) {
                if (enemy.health > 0) {
                    if (isOpponentInSnowballRange(currentWorm, enemy) || isOpponentInBananaRange(currentWorm, enemy) || isOpponentInShootRange(currentWorm, enemy)) {
                        return enemy;
                    }
                }
            }
        }
       return null;
    }


    // Method untuk mendapatkan cell dengan jarak paling dekat menuju tengah (16, 16)
    // Untuk siap menghindari lava pada round 100++, sehingga cacing tidak akan ada di daerah ujung
    private Cell goToMid(List<Cell> surroundCell){
        //int d1 = euclideanDistance(16, 16, surroundCell.get(0).x, surroundCell.get(0).y);
        double d1 = (Math.sqrt(Math.pow(surroundCell.get(0).x - 16, 2) + Math.pow(surroundCell.get(0).y - 16, 2)));
        Cell tempCell = surroundCell.get(0);
        for(int i = 0; i < surroundCell.size(); i++){
            if(gameState.map[surroundCell.get(i).x][surroundCell.get(i).y].powerUp != null) {
                if (gameState.map[surroundCell.get(i).x][surroundCell.get(i).y].powerUp.type == PowerUpType.HEALTH_PACK) {
                    tempCell = surroundCell.get(i);
                    break;
                }
            }
            double newD1 = (Math.sqrt(Math.pow(surroundCell.get(i).x - 16, 2) + Math.pow(surroundCell.get(i).y - 16, 2)));
            if (d1>newD1){ //d1>newD1 && d2>newD2
                d1 = newD1;
                tempCell = surroundCell.get(i);
            }
        }
        return tempCell;
    }

    // Method untuk mendapatkan cell yang mengarah semakin dekat pada cacing musuh
    // Salah satu pengimplementasian strategi greedy yaitu untuk mendapatkan cell yang jaraknya dekat dengan cacing target
    public Cell goToEnemyCell(List<Cell> surroundCell, Worm enemyWorm){
        int d1 = euclideanDistance(enemyWorm.position.x, enemyWorm.position.y, surroundCell.get(0).x, surroundCell.get(0).y);
        Cell tempCell = surroundCell.get(0);
        for(int i = 0; i < surroundCell.size(); i++){
            if(gameState.map[surroundCell.get(i).x][surroundCell.get(i).y].powerUp != null) {
                if (gameState.map[surroundCell.get(i).x][surroundCell.get(i).y].powerUp.type == PowerUpType.HEALTH_PACK) {
                    tempCell = surroundCell.get(i);
                    break;
                }
            }
            //double newD1 = (Math.sqrt(Math.pow(surroundCell.get(i).x - enemyWorm.position.x, 2) + Math.pow(surroundCell.get(i).y - enemyWorm.position.y, 2)));
            int newD1 = euclideanDistance(enemyWorm.position.x, enemyWorm.position.y, surroundCell.get(i).x, surroundCell.get(i).y);
            int d2 = euclideanDistance(otherWorm[0].position.x, otherWorm[0].position.y, surroundCell.get(i).x, surroundCell.get(i).y);
            int d3 = euclideanDistance(otherWorm[1].position.x, otherWorm[1].position.y, surroundCell.get(i).x, surroundCell.get(i).y);
            if (d1>newD1 && d2>2 && d3>2){
                d1 = newD1;
                tempCell = surroundCell.get(i);
            }
        }
        return tempCell;
    }


    // Method untuk mendapatkan jumlah total HP musuh
    private int getOpponentHP(){
        int HP = 0;
        for(Worm enemy: opponent.worms){
            HP = HP + enemy.health;
        }
        return HP;
    }

    public Command run() {
        /*
           Penjelasan singkat strategi yang digunakan:
            - Pada round <= 6 para cacing awalnya akan bergerak menuju ke tengah
            - Lalu setelah itu mencari target musuh jika HP musuh >= 330 maka akan dicari musuh dengan jarak terdekat
              jika HP musuh <330 maka akan dicari musuh dengan HP terendah
            - Setelah itu akan dilakukan pengecekan apakah cacing target ada dijangkauan serangan current worm apa tidak
              Jika iya maka akan diserang dengan urutan prioritas senjata dengan damage tertinggi: Banana bomb, snowball, basic attack
            - Jika tidak maka akan dilakukan pengecekan apakah bisa menggunakan select command atau tidak
              Jika bisa maka akan dicek apakah ada cacing teman dengan yang dalam bahaya, jika ada maka akan dilakukan select command dan menyerang musuh dengan urutan prioritas senjata dengan damage tertinggi
            - Jika tidak maka akan dicek apakah current worm dalam bahaya atau tidak, jika iya maka akan menyerang musuh yang membahayakannya dengan urutan prioritas dari senjata yang paling tinggi damagenya
            - Jika tidak maka current worm akan melakukan command move jika tidak ada teman yang dalam bahaya maka akan bergerak menuju cacing target, jika ada maka akan bergerak menuju cacing musuh yang menyerang teman
            - Jika tidak ada command yang memenuhi maka cacing akan bergerak secara random

          Pemanfaatan strategi greedy:
            - Menargetkan musuh dengan HP atau jarak paling sedikit dengan harapan dapat lebih cepat membunuh musuh
            - Bergerak ke musuh dengan HP atau jarak paling sedikit dengan harapan dapat lebih dekat kepada musuh dan dapat menyerangnya
            - Urutan prioritas senjata dari yang damagenya paling tinggi dengan harapan dapat lebih cepat membunuh musuh
         */
        List<Cell> surroundingBlocks = getSurroundingCells(currentWorm.position.x, currentWorm.position.y);
        if(gameState.currentRound <= 6){ //selama 6 round cacing bergerak menuju tengah (setiap cacing 2 command pertamanya bergerak menuju tengah)
            Cell block2 = goToMid(surroundingBlocks);
            if (block2.type == CellType.AIR) {
                return new MoveCommand(block2.x, block2.y);
            } else if (block2.type == CellType.DIRT) {
                return new DigCommand(block2.x, block2.y);
            }
        }
        Worm target = getClosestEnemyWorm(); //Mencari target yaitu antara cacing dengan jarak terdekat atau cacing dengan HP terkecil
        if(getOpponentHP()<330){
            target = getLeastHPEnemy();
        }
        if(target.health>0) { //Cek jika HP target lebih lebih dari 0
            //Serang target dengan prioritas senjata yang damagenya paling tinggi (jika memenuhi syarat)
            if (currentWorm.id == 2) {
                if (isOpponentInBananaRange(currentWorm, target)) {
                    return new BananaShotCommand(target.position.x, target.position.y);
                }
            }
            if (currentWorm.id == 3) {
                if (isOpponentInSnowballRange(currentWorm, target)) {
                    return new SnowBallCommand(target.position.x, target.position.y);
                }
            }
            //Jika tidak bisa menembak dengan senjata yang damagenya tinggi maka gunakan senjata basic
            if (isOpponentInShootRange(currentWorm, target)) {
                Direction direction = resolveDirection(currentWorm.position, target.position);
                return new ShootCommand(direction);
            }
        }
        //Mengecek jika ada teman yang sedang dalam bahaya

        boolean friendInDanger = isOtherWormInDanger();
        if(gameState.myPlayer.remainingWormSelections>0){
            if(friendInDanger){
                MyWorm friendDanger = getFriendInDanger();
                Worm enemyDanger = getEnemyFriendInDanger();
                String s_command = "";
                if(friendDanger!=null && enemyDanger!=null) {
                    if (friendDanger.id == 2) {
                        if (isOpponentInBananaRange(friendDanger, enemyDanger)) {
                            s_command = String.format("banana %d %d", enemyDanger.position.x, enemyDanger.position.y);
                        }
                    }
                    if (friendDanger.id == 3) {
                        if (isOpponentInSnowballRange(friendDanger, enemyDanger)) {
                            s_command = String.format("snowball %d %d", enemyDanger.position.x, enemyDanger.position.y);
                        }
                    }
                    if (!s_command.equals("")) {
                        return new SelectCommand(friendDanger.id, s_command);
                    }
                }
            }
        }
        //Cek jika cacing saat ini dalam bahaya dan dapatkan musuh yang akan menyerangnya
        Worm enemyCurrDanger = getCurrWormInDanger();
        if(enemyCurrDanger != null){
            if(enemyCurrDanger.health > 0) {
                if (currentWorm.id == 2) {
                    if (isOpponentInBananaRange(currentWorm, enemyCurrDanger)) {
                        return new BananaShotCommand(enemyCurrDanger.position.x, enemyCurrDanger.position.y);
                    }
                }
                if (currentWorm.id == 3) {
                    if (isOpponentInSnowballRange(currentWorm, enemyCurrDanger)) {
                        return new SnowBallCommand(enemyCurrDanger.position.x, enemyCurrDanger.position.y);
                    }
                }
                if (isOpponentInShootRange(currentWorm, enemyCurrDanger)) {
                    Direction direction = resolveDirection(currentWorm.position, enemyCurrDanger.position);
                    return new ShootCommand(direction);
                }
            }
        }

        //Strategi greedy bergerak ke cell menuju target dengan jarak atau HP paling sedikit
        Cell block = goToEnemyCell(surroundingBlocks, target);

        if(friendInDanger){
            Worm newTarget = getEnemyFriendInDanger();
            if(newTarget!=null) {
                block = goToEnemyCell(surroundingBlocks, newTarget);
            }
        }



        if (block.type == CellType.AIR) {
            return new MoveCommand(block.x, block.y);
        } else if (block.type == CellType.DIRT) {
            return new DigCommand(block.x, block.y);
        }

        //Jika tidak ada yang memenuhi maka cacing akan bergerak secara random
        int cellIdx = random.nextInt(surroundingBlocks.size());

        Cell block1 = surroundingBlocks.get(cellIdx);
        if (block1.type == CellType.AIR) {
            return new MoveCommand(block1.x, block1.y);
        } else if (block1.type == CellType.DIRT) {
            return new DigCommand(block1.x, block1.y);
        }

        return new DoNothingCommand();


    }


    // Method untuk mendapatkan musuh pertama yang berada pada range serangan senjata
    private Worm getFirstWormInRange(MyWorm friendWorm) {

        Set<String> cells = constructFireDirectionLines(friendWorm.weapon.range, friendWorm)
                .stream()
                .flatMap(Collection::stream)
                .map(cell -> String.format("%d_%d", cell.x, cell.y))
                .collect(Collectors.toSet());

        for (Worm enemyWorm : opponent.worms) {
            String enemyPosition = String.format("%d_%d", enemyWorm.position.x, enemyWorm.position.y);
            if (cells.contains(enemyPosition) && enemyWorm.health>0) {
                return enemyWorm;
            }
        }

        return null;
    }

    // Method untuk mendapatkan kumpulan cell yang berada pada range serangan command shoot
    private List<List<Cell>> constructFireDirectionLines(int range) {
        List<List<Cell>> directionLines = new ArrayList<>();
        for (Direction direction : Direction.values()) {
            List<Cell> directionLine = new ArrayList<>();
            for (int directionMultiplier = 1; directionMultiplier <= range; directionMultiplier++) {

                int coordinateX = currentWorm.position.x + (directionMultiplier * direction.x);
                int coordinateY = currentWorm.position.y + (directionMultiplier * direction.y);

                if (!isValidCoordinate(coordinateX, coordinateY)) {
                    break;
                }

                if (euclideanDistance(currentWorm.position.x, currentWorm.position.y, coordinateX, coordinateY) > range) {
                    break;
                }

                if (coordinateX == otherWorm[0].position.x && coordinateY == otherWorm[0].position.y){
                    break;
                }

                if (coordinateX == otherWorm[1].position.x && coordinateY == otherWorm[1].position.y){
                    break;
                }

                Cell cell = gameState.map[coordinateY][coordinateX];
                if (cell.type != CellType.AIR) {
                    break;
                }

                directionLine.add(cell);
            }
            directionLines.add(directionLine);
        }

        return directionLines;
    }

    private List<List<Cell>> constructFireDirectionLines(int range, MyWorm friendWorm) {
        List<List<Cell>> directionLines = new ArrayList<>();
        for (Direction direction : Direction.values()) {
            List<Cell> directionLine = new ArrayList<>();
            for (int directionMultiplier = 1; directionMultiplier <= range; directionMultiplier++) {

                int coordinateX = friendWorm.position.x + (directionMultiplier * direction.x);
                int coordinateY = friendWorm.position.y + (directionMultiplier * direction.y);

                if (!isValidCoordinate(coordinateX, coordinateY)) {
                    break;
                }

                if (euclideanDistance(friendWorm.position.x, friendWorm.position.y, coordinateX, coordinateY) > range) {
                    break;
                }

                Cell cell = gameState.map[coordinateY][coordinateX];
                if (cell.type != CellType.AIR) {
                    break;
                }

                directionLine.add(cell);
            }
            directionLines.add(directionLine);
        }

        return directionLines;
    }

    // Mendapatkan cell di disekeliling suatu koordinat
    private List<Cell> getSurroundingCells(int x, int y) {
        ArrayList<Cell> cells = new ArrayList<>();
        for (int i = x - 1; i <= x + 1; i++) {
            for (int j = y - 1; j <= y + 1; j++) {
                // Don't include the current position
                if (i != x && j != y && isValidCoordinate(i, j)) {
                    cells.add(gameState.map[j][i]);
                }
            }
        }

        return cells;
    }

    // Method untuk menentukan jarak dari suatu koordinat ke koordinat yang lain
    private int euclideanDistance(int aX, int aY, int bX, int bY) {
        return (int) (Math.sqrt(Math.pow(aX - bX, 2) + Math.pow(aY - bY, 2)));
    }

    // Method untuk menentukan apakah suatu koordinat valid atau tidak
    private boolean isValidCoordinate(int x, int y) {
        return x >= 0 && x < gameState.mapSize
                && y >= 0 && y < gameState.mapSize;
    }

    // Method untuk menentukan arah musuh untuk keperluan shoot command
    private Direction resolveDirection(Position a, Position b) {
        StringBuilder builder = new StringBuilder();

        int verticalComponent = b.y - a.y;
        int horizontalComponent = b.x - a.x;

        if (verticalComponent < 0) {
            builder.append('N');
        } else if (verticalComponent > 0) {
            builder.append('S');
        }

        if (horizontalComponent < 0) {
            builder.append('W');
        } else if (horizontalComponent > 0) {
            builder.append('E');
        }

        return Direction.valueOf(builder.toString());
    }

}
