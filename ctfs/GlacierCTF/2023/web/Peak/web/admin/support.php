<?php
    include_once "includes/session.php";
?>
<!DOCTYPE html>
<html lang="en">
    <?php 
        include_once "../includes/header.php";
        include_once "../includes/csp.php";
    ?>
    <body>
        <?php include_once "../includes/menu.php"; ?>

        <?php $messages = $pdo->query("SELECT * FROM messages")->fetchAll(PDO::FETCH_ASSOC); ?>
        
        <header class="hero bg-primary text-white text-center py-5">
            <div class="container">
                <h1>Support Requests</h1>
            </div>
        </header>

        <section id="messages" class="py-5">
            <div class="container mt-5">
                <ul class="list-group">
                    <?php if(sizeof($messages) > 0) : ?>
                        <?php foreach ($messages as $message): ?>
                            <li class="list-group-item">
                                <h5 class="mb-1"><?php echo htmlentities($message['title']);?> from 
                                <?php 
                                    $sql = "SELECT u.username
                                    FROM messages m
                                    JOIN users u ON m.user_id = u.id
                                    WHERE m.user_id = :user_id";

                                    $stmt = $pdo->prepare($sql);
                                    $stmt->bindParam(':user_id', $message['user_id'], PDO::PARAM_INT);
                                    $stmt->execute();

                                    $result = $stmt->fetch(PDO::FETCH_ASSOC);

                                    echo htmlentities($result['username']);
                                ?></h5>
                                <a href="/pages/view_message.php?id=<?php echo $message['id']; ?>" name="inbox-header">Inspect Request</a>
                            </li>
                        <?php endforeach; ?>
                    <?php else:?>
                        <div class="container text-center">
                            <h3>No messages available at the moment!</h3>
                        </div>
                    <?php endif;?>
                </ul>
            </div>
        </section>
    </body>
</html>
