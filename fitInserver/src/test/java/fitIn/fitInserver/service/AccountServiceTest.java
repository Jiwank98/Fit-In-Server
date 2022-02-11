package fitIn.fitInserver.service;

import fitIn.fitInserver.domain.Account;
import fitIn.fitInserver.domain.Role;
import fitIn.fitInserver.repository.AccountRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityManager;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;


@RunWith(SpringRunner.class)
@SpringBootTest
@Transactional
public class AccountServiceTest {

    @Autowired
    AccountService accountService;

    @Autowired
    AccountRepository accountRepository;

    @Autowired
    EntityManager em;

    @Test
    public  void 회원가입() throws Exception{

        //given
        Account account = new Account();
        account.setEmail("fitin@naver.com");
        account.setPassword("1234");
        account.setName("fitin");
        account.setRole(Role.USER);
        //when
        Long saveId = accountService.join(account);

        //then
        em.flush();
        assertEquals(account, accountRepository.findOne(saveId));

    }

    @Test(expected = IllegalStateException.class)
    public void 중복_회원_예외() throws Exception{
        //given
        Account account1 = new Account();
        account1.setEmail("fitin@naver.com");
        account1.setPassword("1234");
        account1.setName("fitin");
        account1.setRole(Role.USER);

        Account account2 = new Account();
        account2.setEmail("fitin@naver.com");
        account2.setPassword("1234");
        account2.setName("fitin");
        account2.setRole(Role.USER);

        //when
        accountService.join(account1);

        accountService.join(account2);

        //then
        fail("예외가 발생해야 한다.");

    }


}
